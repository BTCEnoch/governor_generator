#!/usr/bin/env python3
"""
Rate Limit Handler - Handles API rate limiting and backoff strategies
Provides intelligent rate limit detection and adaptive backoff for Anthropic API
"""

import time
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json

class RateLimitHandler:
    """Handles rate limiting and adaptive backoff for API calls"""
    
    def __init__(self, requests_per_minute: int = 60, tokens_per_minute: int = 400000):
        self.requests_per_minute = requests_per_minute
        self.tokens_per_minute = tokens_per_minute
        
        # Tracking windows
        self.request_times = []
        self.token_usage = []
        
        # Rate limit detection
        self.rate_limit_hit = False
        self.backoff_until = None
        self.consecutive_limits = 0
        
        # Adaptive settings
        self.current_delay = 1.0
        self.max_delay = 300.0  # 5 minutes max backoff
        
        logging.info(f"🚦 Rate limit handler initialized")
        logging.info(f"   Requests/min: {requests_per_minute}")
        logging.info(f"   Tokens/min: {tokens_per_minute}")
    
    def can_make_request(self, estimated_tokens: int = 1000) -> bool:
        """Check if we can make a request without hitting rate limits"""
        
        now = datetime.now()
        
        # Clean old entries (older than 1 minute)
        self._cleanup_old_entries(now)
        
        # Check if we're in backoff period
        if self.backoff_until and now < self.backoff_until:
            remaining = (self.backoff_until - now).total_seconds()
            logging.debug(f"⏳ In backoff period, {remaining:.1f}s remaining")
            return False
        
        # Check request rate limit
        if len(self.request_times) >= self.requests_per_minute:
            logging.warning("⚠️ Request rate limit approaching")
            return False
        
        # Check token rate limit
        current_tokens = sum(usage['tokens'] for usage in self.token_usage)
        if current_tokens + estimated_tokens > self.tokens_per_minute:
            logging.warning(f"⚠️ Token rate limit approaching ({current_tokens + estimated_tokens}/{self.tokens_per_minute})")
            return False
        
        return True
    
    def record_request(self, tokens_used: int = 1000, response_headers: Optional[Dict] = None) -> None:
        """Record a successful API request"""
        
        now = datetime.now()
        
        # Record request time
        self.request_times.append(now)
        
        # Record token usage
        self.token_usage.append({
            'timestamp': now,
            'tokens': tokens_used
        })
        
        # Check response headers for rate limit info
        if response_headers:
            self._parse_rate_limit_headers(response_headers)
        
        # Reset rate limit status on successful request
        if self.rate_limit_hit:
            self.rate_limit_hit = False
            self.consecutive_limits = 0
            self.current_delay = 1.0
            logging.info("✅ Rate limit status reset after successful request")
    
    def handle_rate_limit_error(self, error_response: Optional[Dict] = None) -> float:
        """Handle rate limit error and return suggested wait time"""
        
        self.rate_limit_hit = True
        self.consecutive_limits += 1
        
        # Adaptive backoff calculation
        if error_response and 'retry_after' in error_response:
            # Use server-suggested retry time
            wait_time = float(error_response['retry_after'])
            logging.info(f"🚦 Server suggested retry after {wait_time}s")
        else:
            # Calculate exponential backoff
            wait_time = min(self.current_delay * (2 ** self.consecutive_limits), self.max_delay)
            logging.info(f"🚦 Calculated backoff: {wait_time}s (attempt {self.consecutive_limits})")
        
        # Set backoff period
        self.backoff_until = datetime.now() + timedelta(seconds=wait_time)
        
        # Update current delay for next time
        self.current_delay = min(wait_time, self.max_delay)
        
        logging.warning(f"⚠️ Rate limit hit, backing off for {wait_time}s")
        
        return wait_time
    
    def wait_for_rate_limit(self) -> None:
        """Wait until rate limit backoff period is over"""
        
        if not self.backoff_until:
            return
        
        now = datetime.now()
        if now < self.backoff_until:
            wait_time = (self.backoff_until - now).total_seconds()
            
            if wait_time > 0:
                logging.info(f"⏳ Waiting {wait_time:.1f}s for rate limit backoff...")
                time.sleep(wait_time)
        
        # Clear backoff period
        self.backoff_until = None
    
    def get_recommended_delay(self) -> float:
        """Get recommended delay between requests to avoid rate limits"""
        
        now = datetime.now()
        self._cleanup_old_entries(now)
        
        # Calculate current rates
        current_requests = len(self.request_times)
        current_tokens = sum(usage['tokens'] for usage in self.token_usage)
        
        # Calculate delay needed to stay under limits
        request_delay = 60.0 / self.requests_per_minute if current_requests > 0 else 0
        token_delay = 60.0 / (self.tokens_per_minute / 1000) if current_tokens > 0 else 0
        
        recommended_delay = max(request_delay, token_delay, 1.0)  # Minimum 1 second
        
        if self.rate_limit_hit:
            recommended_delay *= 2  # Be more conservative after rate limit
        
        return min(recommended_delay, 10.0)  # Max 10 seconds between requests
    
    def _cleanup_old_entries(self, now: datetime) -> None:
        """Remove entries older than 1 minute"""
        
        cutoff = now - timedelta(minutes=1)
        
        # Clean request times
        self.request_times = [t for t in self.request_times if t > cutoff]
        
        # Clean token usage
        self.token_usage = [u for u in self.token_usage if u['timestamp'] > cutoff]
    
    def _parse_rate_limit_headers(self, headers: Dict) -> None:
        """Parse rate limit information from response headers"""
        
        # Common header names for rate limiting
        rate_limit_headers = [
            'x-ratelimit-remaining',
            'x-ratelimit-limit',
            'x-ratelimit-reset',
            'ratelimit-remaining',
            'ratelimit-limit'
        ]
        
        for header_name in rate_limit_headers:
            if header_name in headers:
                value = headers[header_name]
                logging.debug(f"🔍 Rate limit header {header_name}: {value}")
                
                # Adjust behavior based on remaining requests
                if 'remaining' in header_name:
                    try:
                        remaining = int(value)
                        if remaining < 10:  # Low remaining requests
                            logging.warning(f"⚠️ Low rate limit remaining: {remaining}")
                            self.current_delay = max(self.current_delay, 2.0)
                    except ValueError:
                        pass
    
    def get_rate_limit_status(self) -> Dict[str, Any]:
        """Get current rate limit status and statistics"""
        
        now = datetime.now()
        self._cleanup_old_entries(now)
        
        current_requests = len(self.request_times)
        current_tokens = sum(usage['tokens'] for usage in self.token_usage)
        
        return {
            "rate_limit_active": self.rate_limit_hit,
            "backoff_until": self.backoff_until.isoformat() if self.backoff_until else None,
            "consecutive_limits": self.consecutive_limits,
            "current_requests_per_minute": current_requests,
            "current_tokens_per_minute": current_tokens,
            "request_capacity": f"{current_requests}/{self.requests_per_minute}",
            "token_capacity": f"{current_tokens}/{self.tokens_per_minute}",
            "recommended_delay": self.get_recommended_delay()
        }
    
    def reset_rate_limits(self) -> None:
        """Reset rate limit tracking (for testing or manual intervention)"""
        
        self.request_times = []
        self.token_usage = []
        self.rate_limit_hit = False
        self.backoff_until = None
        self.consecutive_limits = 0
        self.current_delay = 1.0
        
        logging.info("🔄 Rate limit tracking reset")

def test_rate_limit_handler():
    """Test the rate limit handler functionality"""
    
    logging.basicConfig(level=logging.INFO)
    
    # Create handler with low limits for testing
    handler = RateLimitHandler(requests_per_minute=5, tokens_per_minute=10000)
    
    print("🧪 Testing rate limit handler...")
    
    # Test normal operations
    for i in range(3):
        if handler.can_make_request(1000):
            handler.record_request(1000)
            print(f"✅ Request {i+1} allowed")
        else:
            print(f"⚠️ Request {i+1} blocked by rate limits")
    
    # Test rate limit hit
    print("\n🧪 Testing rate limit handling...")
    wait_time = handler.handle_rate_limit_error()
    print(f"🚦 Rate limit backoff: {wait_time}s")
    
    # Test status
    status = handler.get_rate_limit_status()
    print(f"\n📊 Rate limit status:")
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    print("\n🎉 Rate limit handler test completed!")

if __name__ == "__main__":
    test_rate_limit_handler() 
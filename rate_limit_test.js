import http from 'k6/http';
import { sleep, check } from 'k6';
import { Counter } from 'k6/metrics';

export const options = {
  vus: 10,
  duration: '30s',
  thresholds: {
    rate_limited_requests: ['count>0'],
  },
};

const rateLimitedRequests = new Counter('rate_limited_requests');

export default function() {
  const baseUrl = __ENV.BASE_URL || 'http://localhost:5173';
  const username = __ENV.USERNAME || 'demo';
  const password = __ENV.PASSWORD || 'demo123';

  const res = http.post(`${baseUrl}/api/user/jwt/create/`, {
    username,
    password,
  });

  if (res.status === 429) {
    rateLimitedRequests.add(1);
  }
  sleep(1);
}

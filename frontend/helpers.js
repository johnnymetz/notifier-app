import { verifyToken } from 'api';

export const protectRoute = async router => {
  const verified = await verifyToken();
  if (!verified) {
    router.push('/login');
  }
};

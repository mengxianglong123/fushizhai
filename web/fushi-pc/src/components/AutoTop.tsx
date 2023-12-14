import React, { useLayoutEffect } from 'react';  
import { useLocation } from 'react-router-dom';  
  
interface AutoScrollTopProps {  
  children: React.ReactNode;  
}  
  
const AutoScrollTop: React.FC<AutoScrollTopProps> = ({ children }) => {  
  const location = useLocation();  
  
  useLayoutEffect(() => {  
    document.documentElement.scrollTo(0, 0);  
  }, [location.pathname]);  
  
  return <>{children}</>;  
};  
  
export default AutoScrollTop;
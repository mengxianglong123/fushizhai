import ReactDOM from 'react-dom/client'
import "reset-css" // 引入样式重置
import App from './App.tsx'
import './index.css'
import { BrowserRouter } from "react-router-dom";
import AutoScrollTop from './components/AutoTop.tsx';

ReactDOM.createRoot(document.getElementById('root')!).render(
    <BrowserRouter>
        <AutoScrollTop>
            <App />
        </AutoScrollTop>
    </BrowserRouter>
    ,
)

import ReactDOM from 'react-dom/client'
import "reset-css" // 引入样式重置
import App from './App.tsx'
import './index.css'
import { BrowserRouter } from "react-router-dom";

ReactDOM.createRoot(document.getElementById('root')!).render(
    <BrowserRouter>
        <App />
    </BrowserRouter>
    ,
)

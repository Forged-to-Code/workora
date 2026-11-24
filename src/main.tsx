import React from 'react'; import {createRoot} from 'react-dom/client'; import {HashRouter} from 'react-router-dom'; import {createClient} from '@supabase/supabase-js'; import L from 'leaflet'; import 'leaflet/dist/leaflet.css'; import './styles.css'; import App from './App';
const url=import.meta.env.VITE_SUPABASE_URL,key=import.meta.env.VITE_SUPABASE_ANON_KEY;
(globalThis as any).workoraBackend=url&&key?createClient(url,key):null;
(globalThis as any).workoraLeaflet=L;
createRoot(document.getElementById('root')!).render(<HashRouter><App/></HashRouter>);

import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Toaster } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import Index from "./pages/Index";
import Obrigado from "./pages/Obrigado";

const App = () => (
  <TooltipProvider>
    <Toaster />
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Index />} />
        <Route path="/obrigado" element={<Obrigado />} />
      </Routes>
    </BrowserRouter>
  </TooltipProvider>
);

export default App;

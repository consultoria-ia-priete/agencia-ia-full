import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";

const NotFound = () => {
  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col items-center justify-center px-4 text-center">
      <p className="text-xs font-medium tracking-wider text-primary uppercase mb-4">
        Erro 404
      </p>
      <h1 className="text-5xl md:text-6xl font-extrabold tracking-tight mb-4">
        Página não encontrada
      </h1>
      <p className="text-muted-foreground max-w-md mb-8">
        O caminho que você tentou acessar não existe. Volte para o diagnóstico e descubra
        seu perfil ideal de empreendedor digital.
      </p>
      <Link to="/">
        <Button size="lg" className="bg-gradient-to-r from-primary to-[#3a1d12]">
          Fazer o diagnóstico
        </Button>
      </Link>
    </div>
  );
};

export default NotFound;

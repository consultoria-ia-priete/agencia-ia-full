import { Button } from "@/components/ui/button";
import { ArrowRight, Quote } from "lucide-react";

interface TransitionScreenProps {
  text: string;
  onContinue: () => void;
}

export const TransitionScreen = ({ text, onContinue }: TransitionScreenProps) => {
  return (
    <div className="w-full max-w-2xl mx-auto animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="bg-gradient-to-br from-primary/10 via-card to-card border border-primary/30 rounded-2xl p-8 md:p-10 relative overflow-hidden">
        <Quote className="absolute top-4 right-4 w-8 h-8 text-primary/30" />
        <div className="flex items-start gap-4">
          <div className="hidden md:flex w-1 self-stretch bg-gradient-to-b from-primary to-[#D97757] rounded-full" />
          <p className="text-lg md:text-xl leading-relaxed text-foreground italic">
            {text}
          </p>
        </div>
      </div>

      <div className="flex justify-center mt-8">
        <Button
          size="lg"
          onClick={onContinue}
          className="h-12 px-8 text-base font-semibold bg-gradient-to-r from-primary to-[#3a1d12] hover:from-primary hover:to-[#5c2f1f]"
        >
          Continuar
          <ArrowRight className="w-5 h-5 ml-2" />
        </Button>
      </div>
    </div>
  );
};

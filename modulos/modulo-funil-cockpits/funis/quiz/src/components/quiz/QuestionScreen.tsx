import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";
import { ArrowLeft, ArrowRight } from "lucide-react";
import { cn } from "@/lib/utils";
import type { QuizQuestion } from "@/data/quizData";

interface QuestionScreenProps {
  question: QuizQuestion;
  currentStep: number;
  totalSteps: number;
  currentAnswers: string[];
  onAnswer: (selectedOptions: string[]) => void;
  onBack: () => void;
}

export const QuestionScreen = ({
  question,
  currentStep,
  totalSteps,
  currentAnswers,
  onAnswer,
  onBack,
}: QuestionScreenProps) => {
  const [selected, setSelected] = useState<string[]>(currentAnswers);

  useEffect(() => {
    setSelected(currentAnswers);
  }, [question.id, currentAnswers]);

  const isMulti = question.type === "multi";

  const toggleOption = (value: string) => {
    if (isMulti) {
      setSelected((prev) =>
        prev.includes(value) ? prev.filter((v) => v !== value) : [...prev, value]
      );
    } else {
      setSelected([value]);
      setTimeout(() => onAnswer([value]), 200);
    }
  };

  const progress = (currentStep / totalSteps) * 100;
  const canContinue = selected.length > 0;

  return (
    <div className="w-full max-w-2xl mx-auto animate-in fade-in slide-in-from-right-4 duration-500">
      <div className="mb-8">
        <div className="flex justify-between items-center mb-3 text-sm text-muted-foreground">
          <span>
            Pergunta {currentStep} de {totalSteps}
          </span>
          <span>{Math.round(progress)}%</span>
        </div>
        <Progress value={progress} />
      </div>

      <h2 className="text-2xl md:text-3xl font-bold tracking-tight mb-2">{question.title}</h2>
      {question.subtitle && (
        <p className="text-muted-foreground mb-8">{question.subtitle}</p>
      )}
      {isMulti && (
        <p className="text-xs text-primary uppercase tracking-wider mb-6 font-medium">
          Selecione todas as opções que se aplicam
        </p>
      )}

      <div className="space-y-3 mb-8">
        {question.options.map((option) => {
          const isSelected = selected.includes(option.value);
          return (
            <button
              key={option.value}
              type="button"
              onClick={() => toggleOption(option.value)}
              className={cn(
                "w-full text-left p-4 md:p-5 rounded-lg border-2 transition-all flex items-center gap-4",
                "hover:border-primary/60 hover:bg-primary/5",
                isSelected
                  ? "border-primary bg-primary/10 shadow-[0_0_20px_-5px_hsl(var(--primary)_/_0.3)]"
                  : "border-border bg-card"
              )}
            >
              {isMulti && (
                <Checkbox
                  checked={isSelected}
                  onCheckedChange={() => toggleOption(option.value)}
                  onClick={(e) => e.stopPropagation()}
                />
              )}
              <Label className="flex-1 cursor-pointer text-base md:text-lg font-medium">
                {option.label}
              </Label>
            </button>
          );
        })}
      </div>

      <div className="flex justify-between items-center">
        <Button variant="ghost" onClick={onBack}>
          <ArrowLeft className="w-4 h-4 mr-2" />
          Voltar
        </Button>

        {isMulti && (
          <Button
            onClick={() => onAnswer(selected)}
            disabled={!canContinue}
            className="bg-gradient-to-r from-primary to-[#3a1d12] hover:from-primary hover:to-[#5c2f1f]"
          >
            Continuar
            <ArrowRight className="w-4 h-4 ml-2" />
          </Button>
        )}
      </div>
    </div>
  );
};

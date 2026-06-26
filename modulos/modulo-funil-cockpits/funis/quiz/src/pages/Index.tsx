import { useState, useEffect } from "react";
import { EntranceScreen } from "@/components/quiz/EntranceScreen";
import { QuestionScreen } from "@/components/quiz/QuestionScreen";
import { TransitionScreen } from "@/components/quiz/TransitionScreen";
import { LeadCaptureScreen } from "@/components/quiz/LeadCaptureScreen";
import { ResultScreen } from "@/components/quiz/ResultScreen";
import { quizQuestions, getProfileType, type ProfileType } from "@/data/quizData";
import { dispatchQuizEvent } from "@/lib/tracking";

type QuizState = "entrance" | "question" | "transition" | "lead_capture" | "result";

const Index = () => {
  const [quizState, setQuizState] = useState<QuizState>("entrance");
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<number, string[]>>({});
  const [leadData, setLeadData] = useState<{ name: string; email: string; phone: string } | null>(null);
  const [transitionText, setTransitionText] = useState<string>("");
  const [pendingNextIndex, setPendingNextIndex] = useState<number | null>(null);

  useEffect(() => {
    dispatchQuizEvent("quiz_pageview");
  }, []);

  const handleStart = () => {
    dispatchQuizEvent("quiz_started");
    const firstQuestion = quizQuestions[0];
    if (firstQuestion) {
      dispatchQuizEvent(`quiz_step_${firstQuestion.id}`, { step_number: firstQuestion.id });
    }
    setQuizState("question");
    setCurrentQuestionIndex(0);
    setAnswers({});
  };

  const advanceTo = (nextIndex: number) => {
    if (nextIndex < quizQuestions.length) {
      const nextQuestion = quizQuestions[nextIndex];
      dispatchQuizEvent(`quiz_step_${nextQuestion.id}`, { step_number: nextQuestion.id });
      setCurrentQuestionIndex(nextIndex);
      setQuizState("question");
    } else {
      dispatchQuizEvent("quiz_completed");
      setQuizState("lead_capture");
    }
  };

  const handleAnswer = (selectedOptions: string[]) => {
    const currentQuestion = quizQuestions[currentQuestionIndex];
    const newAnswers = { ...answers, [currentQuestion.id]: selectedOptions };
    setAnswers(newAnswers);

    let nextIndex = currentQuestionIndex + 1;
    while (nextIndex < quizQuestions.length) {
      const nextQuestion = quizQuestions[nextIndex];
      if (!nextQuestion.condition || nextQuestion.condition(newAnswers)) {
        break;
      }
      nextIndex++;
    }

    // If the question just answered has interText, show the transition screen.
    if (currentQuestion.interText) {
      setTransitionText(currentQuestion.interText);
      setPendingNextIndex(nextIndex);
      setQuizState("transition");
      return;
    }

    advanceTo(nextIndex);
  };

  const handleTransitionContinue = () => {
    if (pendingNextIndex !== null) {
      const target = pendingNextIndex;
      setPendingNextIndex(null);
      advanceTo(target);
    }
  };

  const handleBack = () => {
    if (currentQuestionIndex === 0) {
      setQuizState("entrance");
      return;
    }

    let prevIndex = currentQuestionIndex - 1;
    while (prevIndex >= 0) {
      const prevQuestion = quizQuestions[prevIndex];
      if (!prevQuestion.condition || prevQuestion.condition(answers)) {
        break;
      }
      prevIndex--;
    }

    if (prevIndex >= 0) {
      setCurrentQuestionIndex(prevIndex);
    } else {
      setQuizState("entrance");
    }
  };

  const handleLeadCapture = (data: { name: string; email: string; phone: string }) => {
    setLeadData(data);
    setQuizState("result");
  };

  // DEV-ONLY preview mode: ?preview=result&profile=especialista&name=Alex
  // Lets the team review the ResultScreen copy without filling the whole quiz.
  // Guarded by import.meta.env.DEV — this branch is dead code in production builds.
  if (import.meta.env.DEV && typeof window !== "undefined") {
    const previewParams = new URLSearchParams(window.location.search);
    if (previewParams.get("preview") === "result") {
      const profile = (previewParams.get("profile") as ProfileType) || "profissional";
      const name = previewParams.get("name") || "Alex";
      return (
        <div className="min-h-screen bg-background text-foreground font-sans selection:bg-primary/30">
          <div className="fixed inset-0 z-0 overflow-hidden pointer-events-none hidden md:block">
            <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-primary/20 rounded-full blur-[120px]" />
            <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-primary/10 rounded-full blur-[120px]" />
          </div>
          <main className="relative z-10 container mx-auto px-4 py-8 md:py-12 min-h-screen flex flex-col justify-center">
            <ResultScreen name={name} profileType={profile} />
          </main>
        </div>
      );
    }
  }

  return (
    <div className="min-h-screen bg-background text-foreground font-sans selection:bg-primary/30">
      <div className="fixed inset-0 z-0 overflow-hidden pointer-events-none hidden md:block">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-primary/20 rounded-full blur-[120px]" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-primary/10 rounded-full blur-[120px]" />
      </div>

      <main className="relative z-10 container mx-auto px-4 py-8 md:py-12 min-h-screen flex flex-col justify-center">
        {quizState === "entrance" && <EntranceScreen onStart={handleStart} />}

        {quizState === "question" && (
          <QuestionScreen
            question={quizQuestions[currentQuestionIndex]}
            currentStep={currentQuestionIndex + 1}
            totalSteps={quizQuestions.length}
            currentAnswers={answers[quizQuestions[currentQuestionIndex].id] || []}
            onAnswer={handleAnswer}
            onBack={handleBack}
          />
        )}

        {quizState === "transition" && (
          <TransitionScreen text={transitionText} onContinue={handleTransitionContinue} />
        )}

        {quizState === "lead_capture" && (
          <LeadCaptureScreen
            onSubmit={handleLeadCapture}
            profileType={getProfileType(answers)}
            answers={answers}
          />
        )}

        {quizState === "result" && leadData && (
          <ResultScreen
            name={leadData.name}
            email={leadData.email}
            phone={leadData.phone}
            profileType={getProfileType(answers)}
          />
        )}
      </main>
    </div>
  );
};

export default Index;

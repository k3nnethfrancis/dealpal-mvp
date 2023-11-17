import { FC } from "react";

interface Props {
  onReset: () => void;
}

export const ResetChat: FC<Props> = ({ onReset }) => {
  return (
    <div className="flex flex-row items-center">
      <button
        className="text-sm sm:text-base text-primary font-semibold rounded-lg px-4 py-2 bg-background hover:bg-neutral-300 focus:outline-none focus:ring-1 focus:ring-primary"
        onClick={() => onReset()}
      >
        Reset
      </button>
    </div>
  );
};
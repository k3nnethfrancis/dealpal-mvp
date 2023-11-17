import { FC } from "react";

export const Navbar: FC = () => {
  return (
    <div className="flex h-[50px] sm:h-[60px] border-b border-neutral-200 py-2 px-2 sm:px-8 items-center justify-between bg-background text-primary">
      <div className="font-bold text-3xl flex items-center">
        <a
          className="ml-2 hover:opacity-50"
          href="https://code-scaffold.vercel.app"
        >
          DealPal AI
        </a>
      </div>
    </div>
  );
};
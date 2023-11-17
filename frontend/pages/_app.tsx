import "@/styles/globals.css";
import "tailwindcss/tailwind.css"; // Import Tailwind CSS
import type { AppProps } from "next/app";
import { Inter } from "next/font/google";

const inter = Inter({ subsets: ["latin"] });

export default function App({ Component, pageProps }: AppProps<{}>) {
  return (
    <main className={`${inter.className} bg-background text-primary`}>
      <Component {...pageProps} />
    </main>
  );
}
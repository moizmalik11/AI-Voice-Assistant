import * as React from "react"
import { motion } from "framer-motion";
 
export function ShiningText({text}) {
  return (
    <motion.h1
      className="bg-[linear-gradient(110deg,#a3a3a3,35%,#fff,50%,#a3a3a3,75%,#a3a3a3)] bg-[length:200%_100%] bg-clip-text text-base font-regular text-transparent"
      initial={{ backgroundPosition: "200% 0" }}
      animate={{ backgroundPosition: "-200% 0" }}
      transition={{
        repeat: Infinity,
        duration: 2,
        ease: "linear",
      }}
    >
      {text}
    </motion.h1>
  );
}

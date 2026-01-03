"use client"

import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"
import { motion, type HTMLMotionProps } from "framer-motion"

import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center whitespace-nowrap rounded-xl text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-luxury-accent-gold disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-luxury-accent-gold text-luxury-background shadow-sm hover:bg-luxury-accent-gold/90",
        destructive:
          "bg-red-500 text-destructive-foreground shadow-sm hover:bg-red-500/90",
        outline:
          "border border-luxury-accent-gold bg-transparent shadow-sm hover:bg-luxury-accent-gold hover:text-luxury-background",
        secondary:
          "bg-luxury-surface text-luxury-text-primary hover:bg-luxury-surface/80",
        ghost: "hover:bg-luxury-surface hover:text-luxury-accent-gold",
        link: "text-luxury-accent-gold underline-offset-4 hover:underline",
      },
      size: {
        default: "h-9 px-4 py-2",
        sm: "h-8 rounded-xl px-3 text-xs",
        lg: "h-11 rounded-xl px-8",
        icon: "h-9 w-9",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

export interface ButtonProps
  extends HTMLMotionProps<"button">,
    VariantProps<typeof buttonVariants> {}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, ...props }, ref) => {
    return (
      <motion.button
        ref={ref}
        whileHover={{ scale: 1.03 }}
        whileTap={{ scale: 0.98 }}
        className={cn(buttonVariants({ variant, size, className }))}
        {...props}
      />
    )
  }
)

Button.displayName = "Button"

export { Button, buttonVariants }

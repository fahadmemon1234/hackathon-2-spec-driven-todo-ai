'use client';

import * as React from 'react';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {}

export const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={`rounded-xl border border-luxury-primary/20 bg-luxury-card text-luxury-text-primary shadow ${className || ''}`}
      {...props}
    />
  )
);

Card.displayName = 'Card';

interface CardContentProps extends React.HTMLAttributes<HTMLDivElement> {}

export const CardContent = React.forwardRef<HTMLDivElement, CardContentProps>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={`p-6 pt-0 ${className || ''}`} {...props} />
  )
);

CardContent.displayName = 'CardContent';

interface CardFooterProps extends React.HTMLAttributes<HTMLDivElement> {}

export const CardFooter = React.forwardRef<HTMLDivElement, CardFooterProps>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={`flex items-center p-6 pt-0 ${className || ''}`}
      {...props}
    />
  )
);

CardFooter.displayName = 'CardFooter';
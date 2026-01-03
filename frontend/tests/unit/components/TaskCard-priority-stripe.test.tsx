// frontend/tests/unit/components/TaskCard-priority-stripe.test.tsx
import React from 'react';
import { render, screen } from '@testing-library/react';
import TaskCard from '@/components/TaskCard';

describe('TaskCard Priority Stripe', () => {
  const baseTask = {
    id: '1',
    title: 'Test Task',
    description: 'Test Description',
    completed: false,
    createdAt: new Date().toISOString(),
    onToggle: jest.fn(),
    onEdit: jest.fn(),
    onDelete: jest.fn(),
  };

  it('displays red stripe for high priority tasks', () => {
    const task = { ...baseTask, priority: 'high' };
    render(<TaskCard {...task} />);
    
    // Check if the card has the high priority border class
    const card = screen.getByRole('region'); // Card is a region role
    expect(card).toHaveClass('border-l-[3px]');
    expect(card).toHaveClass('border-luxury-accent-crimson');
  });

  it('displays gold stripe for medium priority tasks', () => {
    const task = { ...baseTask, priority: 'medium' };
    render(<TaskCard {...task} />);
    
    // Check if the card has the medium priority border class
    const card = screen.getByRole('region');
    expect(card).toHaveClass('border-l-[3px]');
    expect(card).toHaveClass('border-luxury-accent-gold');
  });

  it('displays gray stripe for low priority tasks', () => {
    const task = { ...baseTask, priority: 'low' };
    render(<TaskCard {...task} />);
    
    // Check if the card has the low priority border class
    const card = screen.getByRole('region');
    expect(card).toHaveClass('border-l-[3px]');
    expect(card).toHaveClass('border-luxury-text-secondary');
  });
});
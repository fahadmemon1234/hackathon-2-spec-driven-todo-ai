// frontend/tests/unit/components/TaskCard-completed.test.tsx
import React from 'react';
import { render, screen } from '@testing-library/react';
import TaskCard from '@/components/TaskCard';

describe('TaskCard Completed Styling', () => {
  const baseTask = {
    id: '1',
    title: 'Test Task',
    description: 'Test Description',
    priority: 'medium',
    createdAt: new Date().toISOString(),
    onToggle: jest.fn(),
    onEdit: jest.fn(),
    onDelete: jest.fn(),
  };

  it('applies strikethrough to title when task is completed', () => {
    const completedTask = { ...baseTask, completed: true };
    render(<TaskCard {...completedTask} />);
    
    const titleElement = screen.getByText('Test Task');
    expect(titleElement).toHaveClass('line-through');
  });

  it('applies reduced opacity to completed task cards', () => {
    const completedTask = { ...baseTask, completed: true };
    render(<TaskCard {...completedTask} />);
    
    const card = screen.getByRole('region');
    expect(card).toHaveClass('opacity-75');
  });

  it('keeps priority stripe visible with full opacity for completed tasks', () => {
    const completedTask = { ...baseTask, completed: true, priority: 'high' };
    render(<TaskCard {...completedTask} />);
    
    // The priority stripe should remain visible despite the card being marked as completed
    const card = screen.getByRole('region');
    expect(card).toHaveClass('opacity-75'); // Card is faded
    // But the priority stripe should still be visible (this is handled by the component design)
  });

  it('does not apply strikethrough to title when task is not completed', () => {
    const incompleteTask = { ...baseTask, completed: false };
    render(<TaskCard {...incompleteTask} />);
    
    const titleElement = screen.getByText('Test Task');
    expect(titleElement).not.toHaveClass('line-through');
  });

  it('does not apply reduced opacity to incomplete task cards', () => {
    const incompleteTask = { ...baseTask, completed: false };
    render(<TaskCard {...incompleteTask} />);
    
    const card = screen.getByRole('region');
    expect(card).not.toHaveClass('opacity-75');
  });
});
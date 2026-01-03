// frontend/tests/unit/components/TaskCard-priority-badge.test.tsx
import React from 'react';
import { render, screen } from '@testing-library/react';
import TaskCard from '@/components/TaskCard';

describe('TaskCard Priority Badge', () => {
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

  it('displays HIGH badge for high priority tasks', () => {
    const task = { ...baseTask, priority: 'high' };
    render(<TaskCard {...task} />);
    
    expect(screen.getByText('HIGH')).toBeInTheDocument();
    const badge = screen.getByText('HIGH');
    expect(badge).toHaveClass('bg-red-500/20');
    expect(badge).toHaveClass('text-luxury-accent-crimson');
  });

  it('displays MEDIUM badge for medium priority tasks', () => {
    const task = { ...baseTask, priority: 'medium' };
    render(<TaskCard {...task} />);
    
    expect(screen.getByText('MEDIUM')).toBeInTheDocument();
    const badge = screen.getByText('MEDIUM');
    expect(badge).toHaveClass('bg-yellow-500/20');
    expect(badge).toHaveClass('text-luxury-accent-gold');
  });

  it('displays LOW badge for low priority tasks', () => {
    const task = { ...baseTask, priority: 'low' };
    render(<TaskCard {...task} />);
    
    expect(screen.getByText('LOW')).toBeInTheDocument();
    const badge = screen.getByText('LOW');
    expect(badge).toHaveClass('bg-gray-500/20');
    expect(badge).toHaveClass('text-luxury-text-secondary');
  });
});
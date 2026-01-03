// frontend/tests/unit/components/TaskCard-category.test.tsx
import React from 'react';
import { render, screen } from '@testing-library/react';
import TaskCard from '@/components/TaskCard';

describe('TaskCard Category Tag', () => {
  const baseTask = {
    id: '1',
    title: 'Test Task',
    description: 'Test Description',
    completed: false,
    priority: 'medium',
    createdAt: new Date().toISOString(),
    onToggle: jest.fn(),
    onEdit: jest.fn(),
    onDelete: jest.fn(),
  };

  it('displays category tag when category is provided', () => {
    const task = { ...baseTask, category: 'work' };
    render(<TaskCard {...task} />);
    
    expect(screen.getByText('work')).toBeInTheDocument();
    const categoryTag = screen.getByText('work');
    expect(categoryTag).toHaveClass('rounded-full');
    expect(categoryTag).toHaveClass('bg-luxury-surface');
  });

  it('does not display category tag when category is not provided', () => {
    const task = { ...baseTask, category: undefined };
    render(<TaskCard {...task} />);
    
    expect(screen.queryByText('work')).not.toBeInTheDocument();
    expect(screen.queryByTestId('category-tag')).not.toBeInTheDocument();
  });

  it('hides category tag when category is empty string', () => {
    const task = { ...baseTask, category: '' };
    render(<TaskCard {...task} />);
    
    expect(screen.queryByText('')).not.toBeInTheDocument();
  });
});
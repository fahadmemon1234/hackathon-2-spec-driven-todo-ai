// frontend/tests/unit/components/TaskCard.test.tsx
import React from 'react';
import { render, screen } from '@testing-library/react';
import TaskCard from '@/components/TaskCard';

describe('TaskCard', () => {
  const mockTask = {
    id: '1',
    title: 'Test Task',
    description: 'Test Description',
    completed: false,
    priority: 'medium',
    category: 'work',
    createdAt: new Date().toISOString(),
    onToggle: jest.fn(),
    onEdit: jest.fn(),
    onDelete: jest.fn(),
  };

  it('renders task title and description', () => {
    render(<TaskCard {...mockTask} />);
    expect(screen.getByText('Test Task')).toBeInTheDocument();
    expect(screen.getByText('Test Description')).toBeInTheDocument();
  });

  it('displays priority badge with correct text', () => {
    render(<TaskCard {...mockTask} />);
    expect(screen.getByText('MEDIUM')).toBeInTheDocument();
  });

  it('displays category tag when category is provided', () => {
    render(<TaskCard {...mockTask} />);
    expect(screen.getByText('work')).toBeInTheDocument();
  });

  it('does not display category tag when category is not provided', () => {
    const taskWithoutCategory = { ...mockTask, category: undefined };
    render(<TaskCard {...taskWithoutCategory} />);
    expect(screen.queryByText(mockTask.category)).not.toBeInTheDocument();
  });

  it('applies strikethrough to title when task is completed', () => {
    const completedTask = { ...mockTask, completed: true };
    render(<TaskCard {...completedTask} />);
    const titleElement = screen.getByText('Test Task');
    expect(titleElement).toHaveClass('line-through');
  });
});
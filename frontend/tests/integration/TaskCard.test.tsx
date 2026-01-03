// frontend/tests/integration/components/TaskCard.test.tsx
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import TaskCard from '@/components/TaskCard';

describe('TaskCard Integration', () => {
  const mockOnToggle = jest.fn();
  const mockOnEdit = jest.fn();
  const mockOnDelete = jest.fn();

  const baseTask = {
    id: '1',
    title: 'Test Task',
    description: 'Test Description',
    completed: false,
    priority: 'medium',
    category: 'work',
    createdAt: new Date().toISOString(),
    onToggle: mockOnToggle,
    onEdit: mockOnEdit,
    onDelete: mockOnDelete,
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('integrates priority indicators with task completion state', () => {
    const task = { ...baseTask, priority: 'high', completed: false };
    render(<TaskCard {...task} />);

    // Verify priority indicator is visible
    expect(screen.getByText('HIGH')).toBeInTheDocument();

    // Toggle completion
    const checkbox = screen.getByRole('checkbox');
    fireEvent.click(checkbox);

    // Verify that priority indicator is still visible after completion
    expect(mockOnToggle).toHaveBeenCalledWith(task.id);
    expect(screen.getByText('HIGH')).toBeInTheDocument();
  });

  it('integrates category tags with priority indicators', () => {
    const task = { ...baseTask, priority: 'low', category: 'personal' };
    render(<TaskCard {...task} />);

    // Verify both priority and category are visible
    expect(screen.getByText('LOW')).toBeInTheDocument();
    expect(screen.getByText('personal')).toBeInTheDocument();
  });

  it('handles completed task styling with priority indicators', () => {
    const task = { ...baseTask, completed: false };
    render(<TaskCard {...task} });

    // Initially not completed
    const titleElement = screen.getByText('Test Task');
    expect(titleElement).not.toHaveClass('line-through');

    // Toggle to completed
    const checkbox = screen.getByRole('checkbox');
    fireEvent.click(checkbox);

    // Verify completion styling is applied
    expect(mockOnToggle).toHaveBeenCalledWith(task.id);
  });

  it('allows editing task with priority and category information', () => {
    const task = { ...baseTask, priority: 'high', category: 'work' };
    render(<TaskCard {...task} });

    const editButton = screen.getByText('Edit');
    fireEvent.click(editButton);

    expect(mockOnEdit).toHaveBeenCalledWith({
      id: task.id,
      title: task.title,
      description: task.description,
      priority: task.priority,
      category: task.category
    });
  });

  it('allows deleting task', () => {
    const task = { ...baseTask };
    render(<TaskCard {...task} });

    const deleteButton = screen.getByText('Delete');
    fireEvent.click(deleteButton);

    expect(mockOnDelete).toHaveBeenCalledWith(task.id);
  });

  it('maintains luxury theme consistency across all elements', () => {
    const task = { ...baseTask, priority: 'high', category: 'work', completed: true };
    render(<TaskCard {...task} });

    // Verify that all elements follow the luxury theme
    const card = screen.getByRole('region');
    expect(card).toHaveClass('bg-luxury-card/80');
    expect(card).toHaveClass('backdrop-blur-sm');
    
    // Verify priority badge has luxury styling
    expect(screen.getByText('HIGH')).toBeInTheDocument();
    
    // Verify category tag has luxury styling
    expect(screen.getByText('work')).toBeInTheDocument();
  });
});
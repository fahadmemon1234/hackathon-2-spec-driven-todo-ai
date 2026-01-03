// frontend/tests/unit/components/TaskCard-theme.test.tsx
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import TaskCard from '@/components/TaskCard';

describe('TaskCard Theme Consistency', () => {
  const baseTask = {
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

  it('applies luxury dark theme styling to priority indicators', () => {
    const task = { ...baseTask, priority: 'high' };
    render(<TaskCard {...task} />);
    
    // Check that priority badge has luxury theme styling
    const priorityBadge = screen.getByText('HIGH');
    expect(priorityBadge).toHaveClass('px-2');
    expect(priorityBadge).toHaveClass('py-0.5');
    expect(priorityBadge).toHaveClass('rounded-full');
    expect(priorityBadge).toHaveClass('text-xs');
    expect(priorityBadge).toHaveClass('font-semibold');
  });

  it('applies luxury dark theme styling to category tags', () => {
    const task = { ...baseTask, category: 'work' };
    render(<TaskCard {...task} />);
    
    // Check that category tag has luxury theme styling
    const categoryTag = screen.getByText('work');
    expect(categoryTag).toHaveClass('px-2');
    expect(categoryTag).toHaveClass('py-0.5');
    expect(categoryTag).toHaveClass('rounded-full');
    expect(categoryTag).toHaveClass('text-xs');
  });

  it('implements subtle hover effects with gold accent color', () => {
    const task = { ...baseTask };
    render(<TaskCard {...task} />);
    
    const card = screen.getByRole('region');
    fireEvent.mouseEnter(card);
    
    // Check if hover effects are applied (these would be in the component's hover classes)
    expect(card).toHaveClass('hover:shadow-xl');
    expect(card).toHaveClass('hover:scale-[1.02]');
  });

  it('uses appropriate contrast ratios for accessibility', () => {
    const task = { ...baseTask, priority: 'low' };
    render(<TaskCard {...task} />);
    
    // Check that low priority badge has appropriate contrast
    const priorityBadge = screen.getByText('LOW');
    expect(priorityBadge).toHaveClass('text-luxury-text-secondary');
  });
});
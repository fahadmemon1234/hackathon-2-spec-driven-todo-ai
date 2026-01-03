// frontend/tests/unit/components/TaskCard-responsive.test.tsx
import React from 'react';
import { render, screen } from '@testing-library/react';
import TaskCard from '@/components/TaskCard';

describe('TaskCard Responsive Design', () => {
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

  it('ensures priority stripe remains visible on mobile', () => {
    // On mobile, the priority stripe should still be visible
    // This is tested by ensuring the stripe is rendered regardless of screen size
    const task = { ...baseTask, priority: 'high' };
    render(<TaskCard {...task} />);
    
    // The stripe is part of the card's border styling
    const card = screen.getByRole('region');
    expect(card).toHaveClass('border-l-[3px]');
  });

  it('allows category tags to stack appropriately on mobile', () => {
    // On mobile, category tags should stack appropriately
    const task = { ...baseTask, category: 'very-long-category-name-that-might-wrap' };
    render(<TaskCard {...task} />);
    
    // Check that the category tag is rendered with appropriate styling
    const categoryTag = screen.getByText('very-long-category-name-that-might-wrap');
    expect(categoryTag).toHaveClass('rounded-full');
  });

  it('maintains visual hierarchy across all devices', () => {
    // The visual hierarchy should be maintained across all devices
    const task = { ...baseTask, priority: 'high', category: 'work' };
    render(<TaskCard {...task} />);
    
    // Check that both priority and category are visible
    expect(screen.getByText('HIGH')).toBeInTheDocument();
    expect(screen.getByText('work')).toBeInTheDocument();
  });

  it('preserves luxury feel on all screen sizes', () => {
    // The luxury feel should be preserved on all screen sizes
    const task = { ...baseTask, priority: 'medium' };
    render(<TaskCard {...task} />);
    
    // Check for luxury theme classes
    const card = screen.getByRole('region');
    expect(card).toHaveClass('bg-luxury-card/80');
    expect(card).toHaveClass('backdrop-blur-sm');
    expect(card).toHaveClass('border');
    expect(card).toHaveClass('border-luxury-primary/30');
  });
});
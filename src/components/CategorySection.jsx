import React, { useMemo } from 'react';
import { TodoItem } from './TodoItem';
import './CategorySection.module.css';

const CATEGORY_CONFIG = {
  work: { label: '💼 업무', emoji: '💼', color: '#1976d2' },
  personal: { label: '👤 개인', emoji: '👤', color: '#388e3c' },
  study: { label: '📚 공부', emoji: '📚', color: '#f57c00' }
};

export function CategorySection({ todos, category }) {
  const categoryTodos = useMemo(
    () => todos.filter(todo => todo.category === category),
    [todos, category]
  );

  if (categoryTodos.length === 0) {
    return null;
  }

  const config = CATEGORY_CONFIG[category];
  const completed = categoryTodos.filter(t => t.completed).length;

  return (
    <div className={`category-section category-${category}`}>
      <h3 className="category-title">{config.label}</h3>
      <p className="category-stats">
        {completed}개/{categoryTodos.length}개 완료
      </p>
      <div className="category-items">
        {categoryTodos.map(todo => (
          <TodoItem key={todo.id} todo={todo} />
        ))}
      </div>
    </div>
  );
}

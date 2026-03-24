import React, { useContext, useMemo } from 'react';
import { AppContext } from '../context/AppContext';
import './ProgressBar.module.css';

export function ProgressBar() {
  const { todos } = useContext(AppContext);

  const stats = useMemo(() => {
    const total = todos.length;
    const completed = todos.filter(t => t.completed).length;
    const percentage = total === 0 ? 0 : Math.round((completed / total) * 100);

    return { total, completed, percentage };
  }, [todos]);

  return (
    <div className="progress-section">
      <p className="progress-text">
        전체: {stats.total}개 | 완료: {stats.completed}개
      </p>
      <div className="progress-bar-container">
        <div
          className="progress-bar-fill"
          style={{ width: `${stats.percentage}%` }}
        >
          {stats.percentage > 20 && (
            <span className="progress-bar-text">{stats.percentage}%</span>
          )}
        </div>
      </div>
      <p className="progress-percentage">{stats.percentage}%</p>
    </div>
  );
}

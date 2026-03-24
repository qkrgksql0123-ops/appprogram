import React, { useContext, useState } from 'react';
import { AppContext } from '../context/AppContext';
import './TodoInput.module.css';

export function TodoInput() {
  const { addTodo } = useContext(AppContext);
  const [title, setTitle] = useState('');
  const [category, setCategory] = useState('work');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (title.trim()) {
      addTodo(title, category);
      setTitle('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form className="todo-input-form" onSubmit={handleSubmit}>
      <h3>🆕 새 할 일</h3>
      <input
        type="text"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        onKeyPress={handleKeyPress}
        placeholder="할 일을 입력하세요"
        className="input-title"
        autoFocus
      />
      <select
        value={category}
        onChange={(e) => setCategory(e.target.value)}
        className="input-category"
      >
        <option value="work">💼 업무</option>
        <option value="personal">👤 개인</option>
        <option value="study">📚 공부</option>
      </select>
      <button type="submit" className="btn-add">
        추가
      </button>
    </form>
  );
}

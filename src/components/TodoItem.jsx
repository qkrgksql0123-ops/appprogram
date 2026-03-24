import React, { useContext, useState } from 'react';
import { AppContext } from '../context/AppContext';
import './TodoItem.module.css';

export function TodoItem({ todo }) {
  const { toggleTodo, deleteTodo, editTodo } = useContext(AppContext);
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(todo.title);

  const handleSaveEdit = () => {
    if (editTitle.trim()) {
      editTodo(todo.id, editTitle);
      setIsEditing(false);
    } else {
      setEditTitle(todo.title);
      setIsEditing(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSaveEdit();
    } else if (e.key === 'Escape') {
      setEditTitle(todo.title);
      setIsEditing(false);
    }
  };

  return (
    <div className={`todo-item ${todo.completed ? 'completed' : ''}`}>
      <input
        type="checkbox"
        checked={todo.completed}
        onChange={() => toggleTodo(todo.id)}
        className="todo-checkbox"
      />

      <div className="todo-info">
        {isEditing ? (
          <input
            type="text"
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
            onBlur={handleSaveEdit}
            onKeyPress={handleKeyPress}
            autoFocus
            className="todo-edit-input"
          />
        ) : (
          <>
            <span className="todo-title">{todo.title}</span>
            {todo.date && <span className="todo-date">{todo.date}</span>}
          </>
        )}
      </div>

      {!isEditing && (
        <div className="todo-actions">
          <button
            onClick={() => setIsEditing(true)}
            className="btn-edit"
            title="수정"
          >
            수정
          </button>
          <button
            onClick={() => deleteTodo(todo.id)}
            className="btn-delete"
            title="삭제"
          >
            삭제
          </button>
        </div>
      )}
    </div>
  );
}

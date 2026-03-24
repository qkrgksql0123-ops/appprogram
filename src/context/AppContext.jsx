import React, { createContext, useState, useCallback } from 'react';

export const AppContext = createContext();

export function AppProvider({ children }) {
  const [todos, setTodos] = useState([]);
  const [darkMode, setDarkMode] = useState(false);
  const [user, setUser] = useState(null);
  const [syncStatus, setSyncStatus] = useState('idle'); // 'idle', 'saving', 'saved', 'error'
  const [isLoading, setIsLoading] = useState(false);

  const toggleDarkMode = useCallback(() => {
    setDarkMode(prev => {
      const newValue = !prev;
      localStorage.setItem('darkMode', newValue ? 'true' : 'false');
      return newValue;
    });
  }, []);

  const addTodo = useCallback((title, category) => {
    if (!title.trim()) return;

    const newTodo = {
      id: Date.now(),
      title: title.trim(),
      category,
      completed: false,
      date: new Date().toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
      })
    };

    setTodos(prev => [...prev, newTodo]);
    setSyncStatus('saving');
  }, []);

  const deleteTodo = useCallback((id) => {
    setTodos(prev => prev.filter(todo => todo.id !== id));
    setSyncStatus('saving');
  }, []);

  const toggleTodo = useCallback((id) => {
    setTodos(prev =>
      prev.map(todo =>
        todo.id === id ? { ...todo, completed: !todo.completed } : todo
      )
    );
    setSyncStatus('saving');
  }, []);

  const editTodo = useCallback((id, newTitle) => {
    if (!newTitle.trim()) return;

    setTodos(prev =>
      prev.map(todo =>
        todo.id === id ? { ...todo, title: newTitle.trim() } : todo
      )
    );
    setSyncStatus('saving');
  }, []);

  const value = {
    todos,
    setTodos,
    darkMode,
    toggleDarkMode,
    user,
    setUser,
    syncStatus,
    setSyncStatus,
    isLoading,
    setIsLoading,
    addTodo,
    deleteTodo,
    toggleTodo,
    editTodo,
  };

  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  );
}

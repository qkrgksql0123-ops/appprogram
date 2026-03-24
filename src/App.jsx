import React, { useContext, useEffect, useRef } from 'react';
import { GoogleOAuthProvider, useGoogleLogin } from '@react-oauth/google';
import { AppContext, AppProvider } from './context/AppContext';
import { useGoogleDrive } from './hooks/useGoogleDrive';
import { Header } from './components/Header';
import { ProgressBar } from './components/ProgressBar';
import { TodoInput } from './components/TodoInput';
import { CategorySection } from './components/CategorySection';
import './App.css';

const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID;

function AppContent() {
  const { user, setUser, todos, darkMode } = useContext(AppContext);
  const { initGoogleDrive, logout } = useGoogleDrive();
  const loginCalled = useRef(false);

  const login = useGoogleLogin({
    scope: 'https://www.googleapis.com/auth/drive.appdata',
    onSuccess: async (codeResponse) => {
      try {
        setUser(codeResponse);
        await initGoogleDrive(codeResponse.access_token);
      } catch (error) {
        console.error('로그인 오류:', error);
        alert('로그인에 실패했습니다');
      }
    },
    onError: () => {
      alert('로그인이 실패했습니다');
    },
    flow: 'implicit'
  });

  // 페이지 로드 시 자동 로그인 시도
  useEffect(() => {
    if (!loginCalled.current && !user) {
      loginCalled.current = true;
      const token = localStorage.getItem('google_token');
      if (token) {
        try {
          const parsedToken = JSON.parse(token);
          setUser(parsedToken);
          initGoogleDrive(parsedToken.access_token).catch(() => {
            localStorage.removeItem('google_token');
          });
        } catch (error) {
          localStorage.removeItem('google_token');
        }
      }
    }
  }, []);

  // 토큰 저장
  useEffect(() => {
    if (user) {
      localStorage.setItem('google_token', JSON.stringify(user));
    }
  }, [user]);

  // 다크모드 적용
  useEffect(() => {
    if (darkMode) {
      document.body.classList.add('dark-mode');
    } else {
      document.body.classList.remove('dark-mode');
    }
  }, [darkMode]);

  const handleLogout = () => {
    logout();
    localStorage.removeItem('google_token');
  };

  const handleExport = () => {
    const dataToExport = {
      version: '2.0',
      exportDate: new Date().toISOString(),
      totalTodos: todos.length,
      completedTodos: todos.filter(t => t.completed).length,
      todos: todos
    };

    const jsonString = JSON.stringify(dataToExport, null, 2);
    const blob = new Blob([jsonString], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `tasks_${new Date().getTime()}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);

    alert('할 일이 내보내졌습니다');
  };

  const handleImport = () => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json';
    input.onchange = (e) => {
      const file = e.target.files[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = (event) => {
        try {
          const data = JSON.parse(event.target.result);
          if (data.todos && Array.isArray(data.todos)) {
            alert('가져오기 기능이 구현 중입니다');
          } else {
            alert('올바른 JSON 형식이 아닙니다');
          }
        } catch (error) {
          alert('파일을 읽는 중 오류가 발생했습니다');
        }
      };
      reader.readAsText(file);
    };
    input.click();
  };

  if (!user) {
    return (
      <div className="login-container">
        <div className="login-card">
          <h1>📋 Daily Task Manager</h1>
          <p>Google Drive와 동기화되는 할 일 관리 앱</p>
          <button className="btn-login" onClick={() => login()}>
            🔐 Google로 로그인
          </button>
          <p className="login-info">
            Google Drive에 안전하게 할 일 목록을 저장합니다
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="app-container">
      <Header onLogout={handleLogout} onExport={handleExport} onImport={handleImport} />

      <main className="main-content">
        <div className="content-wrapper">
          <aside className="sidebar">
            <div className="sidebar-panel">
              <h3>📊 할 일 추가</h3>
              <TodoInput />
              <ProgressBar />
            </div>
          </aside>

          <section className="todo-section">
            {todos.length === 0 ? (
              <div className="empty-state">
                <p>📭 등록된 할 일이 없습니다</p>
                <p>좌측 패널에서 새 할 일을 추가하세요</p>
              </div>
            ) : (
              <div className="categories">
                <CategorySection todos={todos} category="work" />
                <CategorySection todos={todos} category="personal" />
                <CategorySection todos={todos} category="study" />
              </div>
            )}
          </section>
        </div>
      </main>
    </div>
  );
}

export default function App() {
  if (!GOOGLE_CLIENT_ID) {
    return (
      <div style={{ padding: '20px', textAlign: 'center' }}>
        <h2>⚠️ Google Client ID가 설정되지 않았습니다</h2>
        <p>
          .env 파일에 <code>VITE_GOOGLE_CLIENT_ID</code>를 설정해주세요
        </p>
      </div>
    );
  }

  return (
    <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID}>
      <AppProvider>
        <AppContent />
      </AppProvider>
    </GoogleOAuthProvider>
  );
}

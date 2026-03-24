import React, { useContext } from 'react';
import { AppContext } from '../context/AppContext';
import './Header.module.css';

export function Header({ onLogout, onExport, onImport }) {
  const { darkMode, toggleDarkMode, user, syncStatus } = useContext(AppContext);

  return (
    <header className="header">
      <div className="header-content">
        <h1>📋 Daily Task Manager</h1>
        <div className="header-controls">
          <button className="btn-icon" onClick={onExport} title="내보내기">
            📥 내보내기
          </button>
          <button className="btn-icon" onClick={onImport} title="가져오기">
            📤 가져오기
          </button>
          <button className="btn-icon" onClick={toggleDarkMode} title="다크모드">
            {darkMode ? '☀️ 라이트' : '🌙 다크'}
          </button>

          {/* 동기화 상태 표시 */}
          <div className={`sync-status ${syncStatus}`}>
            {syncStatus === 'saving' && <span>💾 저장 중...</span>}
            {syncStatus === 'saved' && <span>✅ 저장됨</span>}
            {syncStatus === 'error' && <span>❌ 오류</span>}
            {syncStatus === 'idle' && user && <span>✓ 동기화됨</span>}
          </div>

          {user && (
            <>
              <span className="user-info">
                👤 {user.name}
              </span>
              <button className="btn-logout" onClick={onLogout}>
                로그아웃
              </button>
            </>
          )}
        </div>
      </div>
    </header>
  );
}

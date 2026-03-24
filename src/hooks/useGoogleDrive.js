import { useContext, useCallback, useEffect, useRef } from 'react';
import { AppContext } from '../context/AppContext';
import * as driveHelper from '../utils/driveHelper';

const GAPI_SCRIPT_URL = 'https://apis.google.com/js/api.js';
const GAPI_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID;
const GAPI_DISCOVERY_DOCS = ['https://www.googleapis.com/discovery/v1/apis/drive/v3/rest'];
const GAPI_SCOPES = 'https://www.googleapis.com/auth/drive.appdata';

export function useGoogleDrive() {
  const {
    todos,
    setTodos,
    setUser,
    setSyncStatus,
    setIsLoading
  } = useContext(AppContext);

  const fileIdRef = useRef(null);
  const debounceTimeoutRef = useRef(null);
  const initPromiseRef = useRef(null);

  /**
   * Google API 클라이언트 초기화
   */
  const initGoogleDrive = useCallback(async (accessToken) => {
    if (initPromiseRef.current) {
      return initPromiseRef.current;
    }

    initPromiseRef.current = (async () => {
      try {
        setIsLoading(true);

        // gapi 스크립트 로드
        if (!window.gapi) {
          await new Promise((resolve, reject) => {
            const script = document.createElement('script');
            script.src = GAPI_SCRIPT_URL;
            script.onload = () => {
              window.gapi.load('client', resolve);
            };
            script.onerror = reject;
            document.head.appendChild(script);
          });
        }

        // Drive API 클라이언트 초기화
        await window.gapi.client.init({
          discoveryDocs: GAPI_DISCOVERY_DOCS
        });

        // 토큰 설정
        window.gapi.client.setToken({ access_token: accessToken });

        // todos.json 파일 ID 조회/생성
        const fileId = await driveHelper.getTodosFileId();
        fileIdRef.current = fileId;

        // Drive에서 todos 데이터 로드
        const loadedTodos = await driveHelper.readTodosFile(fileId);
        setTodos(loadedTodos);

        setIsLoading(false);
        setSyncStatus('idle');

        return true;
      } catch (error) {
        console.error('Google Drive 초기화 오류:', error);
        setIsLoading(false);
        setSyncStatus('error');
        initPromiseRef.current = null;
        throw error;
      }
    })();

    return initPromiseRef.current;
  }, [setTodos, setSyncStatus, setIsLoading]);

  /**
   * Drive에 todos 저장 (자동 재시도 1회)
   */
  const saveTodos = useCallback(async (todosToSave) => {
    if (!fileIdRef.current) {
      console.warn('파일 ID가 설정되지 않음');
      setSyncStatus('error');
      return;
    }

    try {
      await driveHelper.writeTodosFile(fileIdRef.current, todosToSave);
      setSyncStatus('saved');

      // 2초 후 idle 상태로 변경
      setTimeout(() => {
        setSyncStatus('idle');
      }, 2000);
    } catch (error) {
      console.error('Drive 저장 오류:', error);
      setSyncStatus('error');

      // 재시도 1회
      setTimeout(async () => {
        try {
          await driveHelper.writeTodosFile(fileIdRef.current, todosToSave);
          setSyncStatus('saved');
          setTimeout(() => {
            setSyncStatus('idle');
          }, 2000);
        } catch (retryError) {
          console.error('Drive 저장 재시도 실패:', retryError);
          setSyncStatus('error');
        }
      }, 1000);
    }
  }, [setSyncStatus]);

  /**
   * todos 변경 시 자동 저장 (debounce 1초)
   */
  useEffect(() => {
    if (!fileIdRef.current) return;

    // 기존 타이머 취소
    if (debounceTimeoutRef.current) {
      clearTimeout(debounceTimeoutRef.current);
    }

    // 새로운 타이머 설정
    debounceTimeoutRef.current = setTimeout(() => {
      setSyncStatus('saving');
      saveTodos(todos);
    }, 1000);

    // 정리: 컴포넌트 언마운트 시 타이머 취소
    return () => {
      if (debounceTimeoutRef.current) {
        clearTimeout(debounceTimeoutRef.current);
      }
    };
  }, [todos, saveTodos, setSyncStatus]);

  /**
   * Drive에서 todos 수동 로드
   */
  const loadTodos = useCallback(async () => {
    if (!fileIdRef.current) {
      console.warn('파일 ID가 설정되지 않음');
      return;
    }

    try {
      setIsLoading(true);
      const loadedTodos = await driveHelper.readTodosFile(fileIdRef.current);
      setTodos(loadedTodos);
      setIsLoading(false);
    } catch (error) {
      console.error('todos 로드 오류:', error);
      setIsLoading(false);
      setSyncStatus('error');
    }
  }, [setTodos, setSyncStatus, setIsLoading]);

  /**
   * 로그아웃
   */
  const logout = useCallback(() => {
    window.gapi.auth2.getAuthInstance().signOut().then(() => {
      setUser(null);
      setTodos([]);
      setSyncStatus('idle');
      fileIdRef.current = null;
      initPromiseRef.current = null;
    });
  }, [setUser, setTodos, setSyncStatus]);

  return {
    initGoogleDrive,
    saveTodos,
    loadTodos,
    logout,
    fileId: fileIdRef.current
  };
}

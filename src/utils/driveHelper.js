/**
 * Google Drive 상호작용을 위한 헬퍼 함수들
 */

const TODOS_FILENAME = 'todos.json';
const TODOS_FILE_ID_STORAGE = 'todos_file_id';

/**
 * 저장할 todos 데이터 구조
 */
export function buildTodosData(todos) {
  return {
    version: '2.0',
    lastModified: new Date().toISOString(),
    todos: todos || []
  };
}

/**
 * todos.json 파일 ID를 localStorage에서 조회
 */
export function getCachedFileId() {
  return localStorage.getItem(TODOS_FILE_ID_STORAGE);
}

/**
 * todos.json 파일 ID를 localStorage에 캐싱
 */
export function cacheFileId(fileId) {
  localStorage.setItem(TODOS_FILE_ID_STORAGE, fileId);
}

/**
 * todos.json 파일 ID를 Drive에서 조회
 * Drive AppData 폴더에서 'todos.json' 검색
 */
export async function findTodosFileId(auth) {
  try {
    const response = await window.gapi.client.drive.files.list({
      spaces: 'appDataFolder',
      fields: 'files(id, name)',
      pageSize: 1,
      q: `name='${TODOS_FILENAME}'`
    });

    const files = response.result.files;
    if (files && files.length > 0) {
      const fileId = files[0].id;
      cacheFileId(fileId);
      return fileId;
    }

    return null;
  } catch (error) {
    console.error('파일 조회 오류:', error);
    throw error;
  }
}

/**
 * Drive AppData 폴더에 todos.json 파일 생성
 */
export async function createTodosFile(auth) {
  try {
    const fileMetadata = {
      name: TODOS_FILENAME,
      parents: ['appDataFolder'],
      mimeType: 'application/json'
    };

    const initialData = buildTodosData([]);

    const response = await window.gapi.client.drive.files.create({
      resource: fileMetadata,
      fields: 'id'
    }, {
      uploadType: 'media',
      body: JSON.stringify(initialData)
    });

    const fileId = response.result.id;
    cacheFileId(fileId);
    return fileId;
  } catch (error) {
    console.error('파일 생성 오류:', error);
    throw error;
  }
}

/**
 * Drive에서 todos.json 파일의 파일 ID 자동 처리
 * - 캐시 확인
 * - Drive에서 검색
 * - 없으면 생성
 */
export async function getTodosFileId(auth) {
  // 1. 캐시 확인
  let fileId = getCachedFileId();
  if (fileId) {
    try {
      // 파일이 정말 존재하는지 확인
      await window.gapi.client.drive.files.get({
        fileId,
        fields: 'id'
      });
      return fileId;
    } catch (error) {
      // 파일이 없으면 캐시 제거
      localStorage.removeItem(TODOS_FILE_ID_STORAGE);
    }
  }

  // 2. Drive에서 검색
  fileId = await findTodosFileId(auth);
  if (fileId) {
    return fileId;
  }

  // 3. 없으면 생성
  return await createTodosFile(auth);
}

/**
 * Drive에서 todos.json 읽기
 */
export async function readTodosFile(fileId) {
  try {
    const response = await window.gapi.client.drive.files.get({
      fileId,
      alt: 'media'
    });

    const data = response.result;
    return data.todos || [];
  } catch (error) {
    console.error('파일 읽기 오류:', error);
    throw error;
  }
}

/**
 * Drive에 todos.json 쓰기 (업데이트)
 */
export async function writeTodosFile(fileId, todos) {
  try {
    const fileContent = buildTodosData(todos);

    await window.gapi.client.request({
      path: `/upload/drive/v3/files/${fileId}`,
      method: 'PATCH',
      params: {
        uploadType: 'media'
      },
      body: JSON.stringify(fileContent)
    });

    return true;
  } catch (error) {
    console.error('파일 쓰기 오류:', error);
    throw error;
  }
}

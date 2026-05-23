export interface SSHKey {
  id: string;
  userId: string;
  label: string;
  encryptedKey: string;
  createdAt: string;
}

// New interface for uploaded files
export interface UploadedFile {
  id: string;
  filename: string;
  fileSize: number;
  createdAt: string;
  isEncrypted: boolean;
}
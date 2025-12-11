/**
 * Chat message types shared between frontend and backend
 */

/**
 * Role of the message sender
 */
export type MessageRole = 'user' | 'assistant';

/**
 * Chat message metadata
 */
export interface MessageMetadata {
  tokens_used?: number;
  model?: string;
  sources?: string[];
  latency_ms?: number;
  [key: string]: any;
}

/**
 * Chat message object
 */
export interface ChatMessage {
  id: string;
  user_id: string;
  thread_id: string;
  role: MessageRole;
  content: string;
  metadata: MessageMetadata;
  created_at: string;
}

/**
 * Send message request
 */
export interface SendMessageRequest {
  thread_id: string;
  content: string;
  selected_text?: string;  // Optional: text selected by user
}

/**
 * Send message response
 */
export interface SendMessageResponse {
  user_message: ChatMessage;
  assistant_message: ChatMessage;
}

/**
 * Thread history request
 */
export interface GetThreadHistoryRequest {
  thread_id: string;
  limit?: number;
  offset?: number;
}

/**
 * Thread history response
 */
export interface GetThreadHistoryResponse {
  messages: ChatMessage[];
  total: number;
  thread_id: string;
}

/**
 * List user threads response
 */
export interface ListThreadsResponse {
  threads: ThreadInfo[];
  total: number;
}

/**
 * Thread information summary
 */
export interface ThreadInfo {
  thread_id: string;
  message_count: number;
  last_message_at: string;
  first_message_preview: string;
}

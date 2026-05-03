<template>
  <div class="chat-wrapper">
    <!-- 聊天容器 -->
    <div class="chat-container">
      <!-- 顶部栏 -->
      <div class="chat-header">
        <div class="header-info">
          <div class="ai-avatar">
            <span class="avatar-emoji">🤖</span>
            <div class="status-dot"></div>
          </div>
          <div class="ai-info">
            <h3 class="ai-name">农业智能助手</h3>
            <p class="ai-status">
              <span v-if="conversationCount > 0">
                对话 {{ conversationCount }}/{{ maxConversationTurns }}
              </span>
              <span v-else>随时为您提供帮助</span>
            </p>
          </div>
        </div>
        
        <div class="header-actions">
          <button class="action-btn" @click="handleNewSession" title="新对话">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M12 5v14M5 12h14" stroke-width="2" stroke-linecap="round"/>
            </svg>
            <span>新对话</span>
          </button>
          <button class="action-btn danger" @click="handleClear" title="清空">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" stroke-width="2"/>
            </svg>
            <span>清空</span>
          </button>
        </div>
      </div>
      
      <!-- 消息列表 -->
      <div ref="messageListRef" class="message-list">
        <!-- 空状态 -->
        <div v-if="messages.length === 0" class="empty-state">
          <div class="empty-visual">
            <div class="floating-icons">
              <span class="icon icon-1">🌾</span>
              <span class="icon icon-2">🌿</span>
              <span class="icon icon-3">🌱</span>
            </div>
            <div class="center-icon">🤖</div>
          </div>
          <h3 class="empty-title">开始智能对话</h3>
          <p class="empty-description">我是您的农业智能助手，可以帮助您解答种植、病虫害防治、农事管理等问题</p>
          
          <div class="quick-questions">
            <p class="quick-title">快捷提问</p>
            <div class="question-grid">
              <button 
                class="question-card"
                @click="askQuestion('当前有哪些种植计划？')"
              >
                <span class="question-icon">📋</span>
                <span class="question-text">种植计划查询</span>
              </button>
              <button 
                class="question-card"
                @click="askQuestion('最近的病虫害情况如何？')"
              >
                <span class="question-icon">🔍</span>
                <span class="question-text">病虫害诊断</span>
              </button>
              <button 
                class="question-card"
                @click="askQuestion('给我一些种植建议')"
              >
                <span class="question-icon">💡</span>
                <span class="question-text">种植建议</span>
              </button>
              <button 
                class="question-card"
                @click="askQuestion('如何提高作物产量？')"
              >
                <span class="question-icon">📈</span>
                <span class="question-text">产量优化</span>
              </button>
            </div>
          </div>
        </div>
        
        <!-- 消息内容 -->
        <div v-else class="messages-container">
          <div 
            v-for="(message, index) in messages" 
            :key="index" 
            class="message-item"
            :class="message.role"
          >
            <!-- AI 消息 -->
            <template v-if="message.role === 'assistant'">
              <div class="message-avatar ai">
                <span>🤖</span>
              </div>
              <div class="message-bubble ai">
                <div class="message-text" v-html="formatMessage(message.content)"></div>
                <div class="message-meta">
                  <span class="message-time">{{ formatTime(message.timestamp) }}</span>
                </div>
              </div>
            </template>
            
            <!-- 用户消息 -->
            <template v-else>
              <div class="message-bubble user">
                <div class="message-text">{{ message.content }}</div>
                <div class="message-meta">
                  <span class="message-time">{{ formatTime(message.timestamp) }}</span>
                </div>
              </div>
              <div class="message-avatar user">
                <span>👨‍🌾</span>
              </div>
            </template>
          </div>
          
          <!-- 加载中状态 -->
          <div v-if="loading" class="message-item assistant loading-message">
            <div class="message-avatar ai">
              <span>🤖</span>
            </div>
            <div class="message-bubble ai">
              <div class="typing-indicator">
                <span class="dot"></span>
                <span class="dot"></span>
                <span class="dot"></span>
              </div>
              <p class="loading-text">AI 正在思考...</p>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 输入区域 -->
      <div class="input-area">
        <div class="input-container">
          <textarea
            v-model="inputMessage"
            class="message-input"
            :rows="3"
            placeholder="输入您的问题... (Enter发送, Shift+Enter换行)"
            @keydown.enter.prevent="handleEnter"
          ></textarea>
          
          <button 
            class="send-button"
            :disabled="loading || !inputMessage.trim()"
            @click="handleSend"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>发送</span>
          </button>
        </div>
        
        <div class="input-hint">
          <span>💡 提示：可以询问种植建议、病虫害防治、农事安排等问题</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { aiApi } from '@/api/ai'

const messageListRef = ref(null)
const loading = ref(false)
const inputMessage = ref('')
const messages = ref([])
const sessionId = ref('')
const conversationCount = ref(0)
const maxConversationTurns = ref(20)

const generateSessionId = () => {
  return `session-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
}

const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  return `${hours}:${minutes}`
}

const formatMessage = (content) => {
  if (!content) return ''
  return content
    .replace(/\n/g, '<br>')
    .replace(/### (.*)/g, '<strong style="color:#22c55e">$1</strong>')
    .replace(/## (.*)/g, '<strong style="font-size:15px;color:#166534">$1</strong>')
    .replace(/- (.*)/g, '• $1')
}

const scrollToBottom = async () => {
  await nextTick()
  if (messageListRef.value) {
    messageListRef.value.scrollTop = messageListRef.value.scrollHeight
  }
}

const loadHistory = async () => {
  try {
    const response = await aiApi.getHistory({ sessionId: sessionId.value, page: 1, size: 50 })
    if (response.data && response.data.length > 0) {
      const historyMessages = []
      response.data.forEach(item => {
        historyMessages.push({
          role: 'user',
          content: item.question,
          timestamp: new Date(item.createdTime).getTime()
        })
        historyMessages.push({
          role: 'assistant',
          content: item.answer,
          timestamp: new Date(item.createdTime).getTime() + 1
        })
      })
      messages.value = historyMessages.sort((a, b) => a.timestamp - b.timestamp)
      conversationCount.value = response.data.length
      await scrollToBottom()
    }
  } catch (error) {
    console.error('加载历史对话失败:', error)
  }
}

const handleSend = async () => {
  const message = inputMessage.value.trim()
  if (!message) {
    ElMessage.warning('请输入消息内容')
    return
  }

  messages.value.push({
    role: 'user',
    content: message,
    timestamp: Date.now()
  })
  inputMessage.value = ''
  await scrollToBottom()

  loading.value = true
  try {
    const response = await aiApi.sendChatMessage({
      sessionId: sessionId.value,
      message: message
    })

    messages.value.push({
      role: 'assistant',
      content: response.data.reply,
      timestamp: Date.now()
    })
    
    sessionId.value = response.data.sessionId
    conversationCount.value = response.data.conversationCount || conversationCount.value + 1
    maxConversationTurns.value = response.data.maxConversationTurns || 20
    
    if (conversationCount.value >= maxConversationTurns.value) {
      ElMessage.info('已达到对话上限，下次将开启新对话')
    }
    
    await scrollToBottom()
  } catch (error) {
    console.error('发送消息失败:', error)
    ElMessage.error('发送消息失败，请重试')
    messages.value.pop()
  } finally {
    loading.value = false
  }
}

const handleEnter = (event) => {
  if (event.shiftKey) return
  handleSend()
}

const askQuestion = (question) => {
  inputMessage.value = question
  handleSend()
}

const handleNewSession = () => {
  sessionId.value = generateSessionId()
  messages.value = []
  conversationCount.value = 0
  ElMessage.success('已开启新对话')
}

const handleClear = () => {
  ElMessageBox.confirm('确定要清空对话吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
    .then(() => {
      messages.value = []
      sessionId.value = generateSessionId()
      conversationCount.value = 0
      ElMessage.success('对话已清空')
    })
    .catch(() => {})
}

onMounted(() => {
  sessionId.value = generateSessionId()
  loadHistory()
})
</script>

<style scoped>
@import '@/assets/styles/design-system.css';

/* ========================================
   聊天容器
   ======================================== */
.chat-wrapper {
  height: calc(100vh - 140px);
  display: flex;
  flex-direction: column;
  animation: slide-up 0.6s ease-out;
}

.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: var(--radius-2xl);
  box-shadow: var(--shadow-xl);
  overflow: hidden;
}

/* ========================================
   顶部栏
   ======================================== */
.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-4) var(--space-6);
  background: linear-gradient(135deg, var(--primary-50) 0%, white 100%);
  border-bottom: 1px solid var(--soil-200);
}

.header-info {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.ai-avatar {
  position: relative;
  width: 48px;
  height: 48px;
  border-radius: var(--radius-full);
  background: linear-gradient(135deg, var(--primary-400), var(--primary-600));
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-md);
}

.avatar-emoji {
  font-size: 28px;
  animation: float 3s ease-in-out infinite;
}

.status-dot {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--success);
  border: 2px solid white;
  animation: pulse-glow 2s ease-in-out infinite;
}

.ai-info {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.ai-name {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: 600;
  color: var(--soil-800);
  margin: 0;
}

.ai-status {
  font-size: var(--text-sm);
  color: var(--soil-500);
  margin: 0;
}

.header-actions {
  display: flex;
  gap: var(--space-3);
}

.action-btn {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-4);
  background: white;
  border: 1px solid var(--soil-300);
  border-radius: var(--radius-lg);
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--soil-700);
  cursor: pointer;
  transition: all var(--transition-base);
}

.action-btn:hover {
  background: var(--primary-50);
  border-color: var(--primary-400);
  color: var(--primary-700);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.action-btn.danger:hover {
  background: #fef2f2;
  border-color: var(--danger);
  color: var(--danger);
}

/* ========================================
   消息列表
   ======================================== */
.message-list {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-6);
  background: 
    radial-gradient(at 20% 30%, rgba(134, 239, 172, 0.05) 0%, transparent 50%),
    radial-gradient(at 80% 70%, rgba(254, 243, 199, 0.05) 0%, transparent 50%),
    var(--soil-100);
}

/* 空状态 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-12) var(--space-8);
  text-align: center;
  animation: grow 0.6s var(--transition-bounce);
}

.empty-visual {
  position: relative;
  width: 150px;
  height: 150px;
  margin-bottom: var(--space-6);
}

.floating-icons {
  position: absolute;
  width: 100%;
  height: 100%;
}

.icon {
  position: absolute;
  font-size: 40px;
  opacity: 0.3;
  animation: float 4s ease-in-out infinite;
}

.icon-1 {
  top: 0;
  left: 10%;
  animation-delay: 0s;
}

.icon-2 {
  top: 20%;
  right: 10%;
  animation-delay: 1s;
}

.icon-3 {
  bottom: 10%;
  left: 50%;
  transform: translateX(-50%);
  animation-delay: 2s;
}

.center-icon {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 80px;
  filter: drop-shadow(0 10px 20px rgba(0, 0, 0, 0.1));
  animation: pulse-glow 3s ease-in-out infinite;
}

.empty-title {
  font-family: var(--font-display);
  font-size: var(--text-2xl);
  font-weight: 600;
  color: var(--soil-800);
  margin: 0 0 var(--space-3);
}

.empty-description {
  font-size: var(--text-base);
  color: var(--soil-600);
  max-width: 500px;
  margin: 0 0 var(--space-8);
  line-height: 1.6;
}

.quick-questions {
  width: 100%;
  max-width: 600px;
}

.quick-title {
  font-size: var(--text-sm);
  font-weight: 600;
  color: var(--soil-700);
  margin: 0 0 var(--space-4);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.question-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: var(--space-3);
}

.question-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-4);
  background: white;
  border: 2px solid var(--soil-200);
  border-radius: var(--radius-xl);
  cursor: pointer;
  transition: all var(--transition-base);
}

.question-card:hover {
  background: var(--primary-50);
  border-color: var(--primary-400);
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.question-icon {
  font-size: 32px;
}

.question-text {
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--soil-700);
}

/* ========================================
   消息项
   ======================================== */
.messages-container {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.message-item {
  display: flex;
  gap: var(--space-3);
  animation: slide-up 0.4s ease-out;
}

.message-item.user {
  flex-direction: row;
  justify-content: flex-end;
}

.message-item.assistant {
  flex-direction: row;
  justify-content: flex-start;
}

.message-avatar {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  font-size: 24px;
  box-shadow: var(--shadow-sm);
}

.message-avatar.ai {
  background: linear-gradient(135deg, var(--primary-400), var(--primary-600));
}

.message-avatar.user {
  background: linear-gradient(135deg, var(--earth-300), var(--earth-500));
}

.message-bubble {
  max-width: 70%;
  padding: var(--space-4);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-md);
  animation: grow 0.3s var(--transition-bounce);
}

.message-bubble.ai {
  background: white;
  border: 1px solid var(--soil-200);
}

.message-bubble.user {
  background: linear-gradient(135deg, var(--primary-500), var(--primary-600));
  color: white;
}

.message-text {
  font-size: var(--text-base);
  line-height: 1.6;
  word-wrap: break-word;
}

.message-bubble.ai .message-text {
  color: var(--soil-800);
}

.message-meta {
  display: flex;
  justify-content: flex-end;
  margin-top: var(--space-2);
}

.message-time {
  font-size: var(--text-xs);
  color: var(--soil-500);
}

.message-bubble.user .message-time {
  color: rgba(255, 255, 255, 0.8);
}

/* 加载中动画 */
.loading-message {
  animation: none;
}

.typing-indicator {
  display: flex;
  gap: var(--space-1);
  margin-bottom: var(--space-2);
}

.typing-indicator .dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--primary-500);
  animation: typing 1.4s infinite ease-in-out;
}

.typing-indicator .dot:nth-child(1) { animation-delay: 0s; }
.typing-indicator .dot:nth-child(2) { animation-delay: 0.2s; }
.typing-indicator .dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes typing {
  0%, 60%, 100% { transform: translateY(0); opacity: 0.5; }
  30% { transform: translateY(-10px); opacity: 1; }
}

.loading-text {
  font-size: var(--text-sm);
  color: var(--soil-500);
  margin: 0;
}

/* ========================================
   输入区域
   ======================================== */
.input-area {
  padding: var(--space-4) var(--space-6);
  background: white;
  border-top: 1px solid var(--soil-200);
}

.input-container {
  display: flex;
  gap: var(--space-3);
  align-items: flex-end;
}

.message-input {
  flex: 1;
  padding: var(--space-3) var(--space-4);
  background: var(--soil-50);
  border: 2px solid var(--soil-200);
  border-radius: var(--radius-xl);
  font-family: var(--font-body);
  font-size: var(--text-base);
  color: var(--soil-800);
  resize: none;
  transition: all var(--transition-base);
}

.message-input:hover {
  border-color: var(--soil-300);
}

.message-input:focus {
  outline: none;
  border-color: var(--primary-500);
  background: white;
  box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.1);
}

.message-input::placeholder {
  color: var(--soil-400);
}

.send-button {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-6);
  background: linear-gradient(135deg, var(--primary-500), var(--primary-600));
  border: none;
  border-radius: var(--radius-xl);
  font-size: var(--text-base);
  font-weight: 600;
  color: white;
  cursor: pointer;
  transition: all var(--transition-base);
  box-shadow: 
    0 4px 15px rgba(34, 197, 94, 0.3),
    inset 0 -2px 5px rgba(0, 0, 0, 0.1);
}

.send-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 
    0 8px 25px rgba(34, 197, 94, 0.4),
    inset 0 -2px 5px rgba(0, 0, 0, 0.1);
}

.send-button:active:not(:disabled) {
  transform: translateY(0);
}

.send-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.input-hint {
  margin-top: var(--space-2);
  font-size: var(--text-xs);
  color: var(--soil-500);
}

/* ========================================
   滚动条
   ======================================== */
.message-list::-webkit-scrollbar {
  width: 8px;
}

.message-list::-webkit-scrollbar-track {
  background: transparent;
}

.message-list::-webkit-scrollbar-thumb {
  background: var(--soil-300);
  border-radius: var(--radius-full);
}

.message-list::-webkit-scrollbar-thumb:hover {
  background: var(--soil-400);
}
</style>

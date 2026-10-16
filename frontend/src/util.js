const rawBase = import.meta.env.VITE_API_BASE_URL || "https://choose-your-own-adventure-ugyp.onrender.com/api"
const cleanBase = rawBase.trim().replace(/\/+$/, "")
export const API_BASE_URL = cleanBase.endsWith("/api") ? cleanBase : `${cleanBase}/api`
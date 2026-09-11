'use client'

import { createContext, useContext, useEffect, useState, type ReactNode } from 'react'
import api from './api'
import type { Language, Role, User } from './types'

interface RegisterPayload {
  name: string
  email: string
  password: string
  phone?: string
  role: Role
  language: Language
}

interface AuthContextValue {
  user: User | null
  loading: boolean
  initializing: boolean
  login: (email: string, password: string) => Promise<User>
  register: (payload: RegisterPayload) => Promise<User>
  logout: () => void
  setLanguage: (lang: Language) => void
}

const AuthContext = createContext<AuthContextValue | null>(null)

const TOKEN_KEY = 'farmalyze_token'
const USER_KEY = 'farmalyze_user'

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(false)
  const [initializing, setInitializing] = useState(true)

  useEffect(() => {
    const savedUser = window.localStorage.getItem(USER_KEY)
    const token = window.localStorage.getItem(TOKEN_KEY)
    if (savedUser && token) {
      try {
        setUser(JSON.parse(savedUser))
      } catch {
        setUser(null)
      }
    }
    setInitializing(false)
  }, [])

  const login = async (email: string, password: string) => {
    setLoading(true)
    try {
      const { data } = await api.post('/auth/login', { email, password })
      window.localStorage.setItem(TOKEN_KEY, data.access_token)
      window.localStorage.setItem(USER_KEY, JSON.stringify(data.user))
      setUser(data.user)
      return data.user as User
    } finally {
      setLoading(false)
    }
  }

  const register = async (payload: RegisterPayload) => {
    setLoading(true)
    try {
      const { data } = await api.post('/auth/register', payload)
      window.localStorage.setItem(TOKEN_KEY, data.access_token)
      window.localStorage.setItem(USER_KEY, JSON.stringify(data.user))
      setUser(data.user)
      return data.user as User
    } finally {
      setLoading(false)
    }
  }

  const logout = () => {
    window.localStorage.removeItem(TOKEN_KEY)
    window.localStorage.removeItem(USER_KEY)
    setUser(null)
  }

  const setLanguage = (lang: Language) => {
    if (!user) return
    const updated = { ...user, language: lang }
    setUser(updated)
    window.localStorage.setItem(USER_KEY, JSON.stringify(updated))
  }

  return (
    <AuthContext.Provider value={{ user, loading, initializing, login, register, logout, setLanguage }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}

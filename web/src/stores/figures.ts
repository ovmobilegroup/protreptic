import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../api/client'

export interface Figure {
  code: string
  name: string
  description: string
  modes: number[]
  reason: string
  steps: string[]
  expected: string
  case: string
  era: string | null
  historical_domains: string[]
  domains: string[]
  gender: string | null
  ethnicity: string | null
  // International fields
  nationality?: string
  civilization_sphere?: string
  time_period_standardized?: string
  wiki_id?: string
  primary_language?: string
  intellectual_tradition?: string
  cross_cultural_impact?: string
}

export interface FigureListResponse {
  success: boolean
  data: Figure[]
  meta: {
    total: number
    page: number
    page_size: number
    total_pages: number
  }
}

export interface FiguresParams {
  page?: number
  page_size?: number
  search?: string
  lang?: string
  era?: string
  historical_domain?: string
  domain?: string
  gender?: string
  ethnicity?: string
  theme?: string  // P4 theme filtering: TECH/WOMEN/ETHNIC/MED/COMP
  // International filters
  nationality?: string
  civilization_sphere?: string
  time_period_standardized?: string
  wiki_id?: string
  primary_language?: string
  intellectual_tradition?: string
  cross_cultural_impact?: string
}

export interface SemanticSearchResponse {
  success: boolean
  data: any[]
  meta: {
    total: number
    query: string
    search_type: string
    model: string
  }
}

export interface SimilarResponse {
  success: boolean
  data: any[]
  meta: {
    total: number
    source_code: string
    search_type: string
  }
}

export const useFiguresStore = defineStore('figures', () => {
  const figures = ref<Figure[]>([])
  const total = ref(0)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const fetchFigures = async (params: FiguresParams = {}) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.get<FigureListResponse>('/api/v1/scenarios', { params })
      figures.value = response.data.data
      total.value = response.data.meta.total
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch figures'
      console.error('Fetch figures error:', err)
    } finally {
      loading.value = false
    }
  }

  const fetchFigure = async (code: string, lang = 'zh') => {
    loading.value = true
    error.value = null
    try {
      const response = await api.get(`/api/v1/scenarios/${code}`, { params: { lang } })
      return response.data.data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch figure'
      console.error('Fetch figure error:', err)
      return null
    } finally {
      loading.value = false
    }
  }

  const searchFigures = async (query: string, lang = 'zh', limit = 20) => {
    try {
      const response = await api.get('/api/v1/scenarios/search', { params: { q: query, lang, limit } })
      return response.data.data
    } catch (err) {
      console.error('Search figures error:', err)
      return []
    }
  }

  // Enhanced semantic search with new API endpoints
  const semanticSearch = async (query: string, lang = 'zh', topK = 10) => {
    try {
      const response = await api.get<SemanticSearchResponse>('/api/v1/scenarios/semantic-search', {
        params: { q: query, lang, top_k: topK }
      })
      return response.data.data || []
    } catch (err) {
      console.error('Semantic search error:', err)
      return []
    }
  }

  // Similar figures with enhanced similarity scoring for new figures
  const getSimilar = async (code: string, lang = 'zh', topK = 5) => {
    try {
      const response = await api.get<SimilarResponse>(`/api/v1/scenarios/${code}/similar`, {
        params: { lang, top_k: topK }
      })
      return response.data.data || []
    } catch (err) {
      console.error('Similar figures error:', err)
      return []
    }
  }

  // Enhanced similarity search for batch H-322 to H-361
  const getSimilarFromBatch = async (code: string, lang = 'zh', topK = 8) => {
    try {
      const response = await api.get(`/api/v1/scenarios/batch/${code}/similar`, {
        params: { lang, top_k: topK }
      })
      return response.data || []
    } catch (err) {
      console.error('Batch similar search error:', err)
      return []
    }
  }

  return {
    figures,
    total,
    loading,
    error,
    fetchFigures,
    fetchFigure,
    searchFigures,
    semanticSearch,
    getSimilar,
  }
})
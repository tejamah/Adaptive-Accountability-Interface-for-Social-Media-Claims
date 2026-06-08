import { mockPosts } from '../data/mockPosts'

const STORAGE_KEY = 'adaptive-accountability-posts-v1'
const REVIEW_KEY = 'adaptive-accountability-reviews-v1'
const STUDY_KEY = 'adaptive-accountability-study-v1'

const clone = (value) => JSON.parse(JSON.stringify(value))

export function loadPosts() {
  try {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (!stored) return clone(mockPosts)
    const savedPosts = JSON.parse(stored)
    const savedById = new Map(savedPosts.map((post) => [post.id, post]))
    return mockPosts.map((seedPost) => {
      const saved = savedById.get(seedPost.id)
      if (!saved) return clone(seedPost)
      return {
        ...clone(seedPost),
        ...saved,
        requests: saved.requests || clone(seedPost.requests),
        response: saved.response
          ? { ...clone(seedPost.response || {}), ...saved.response }
          : seedPost.response,
      }
    })
  } catch {
    return clone(mockPosts)
  }
}

export function savePosts(posts) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(posts))
}

export function loadReviews() {
  try {
    return JSON.parse(localStorage.getItem(REVIEW_KEY) || '{}')
  } catch {
    return {}
  }
}

export function saveReviews(reviews) {
  localStorage.setItem(REVIEW_KEY, JSON.stringify(reviews))
}

export function loadStudyResponses() {
  try {
    return JSON.parse(localStorage.getItem(STUDY_KEY) || '[]')
  } catch {
    return []
  }
}

export function saveStudyResponses(responses) {
  localStorage.setItem(STUDY_KEY, JSON.stringify(responses))
}

export function resetDemo() {
  localStorage.removeItem(STORAGE_KEY)
  localStorage.removeItem(REVIEW_KEY)
  localStorage.removeItem(STUDY_KEY)
}

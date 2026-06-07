import { mockPosts } from '../data/mockPosts'

const STORAGE_KEY = 'adaptive-accountability-posts-v1'
const REVIEW_KEY = 'adaptive-accountability-reviews-v1'

const clone = (value) => JSON.parse(JSON.stringify(value))

export function loadPosts() {
  try {
    const stored = localStorage.getItem(STORAGE_KEY)
    return stored ? JSON.parse(stored) : clone(mockPosts)
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

export function resetDemo() {
  localStorage.removeItem(STORAGE_KEY)
  localStorage.removeItem(REVIEW_KEY)
}

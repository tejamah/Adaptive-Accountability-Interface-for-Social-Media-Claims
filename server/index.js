import cors from 'cors'
import express from 'express'
import { readFile, writeFile } from 'node:fs/promises'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = dirname(fileURLToPath(import.meta.url))
const dataPath = join(__dirname, 'data.json')
const seedPath = join(__dirname, 'mock-data.json')
const app = express()
const port = process.env.PORT || 3001
const requestThreshold = 5

app.use(cors())
app.use(express.json({ limit: '100kb' }))

async function readData() {
  try {
    return JSON.parse(await readFile(dataPath, 'utf8'))
  } catch {
    const seed = JSON.parse(await readFile(seedPath, 'utf8'))
    await writeFile(dataPath, JSON.stringify(seed, null, 2))
    return seed
  }
}

async function saveData(data) {
  await writeFile(dataPath, JSON.stringify(data, null, 2))
}

app.get('/api/health', (_request, response) => {
  response.json({ status: 'ok', service: 'adaptive-accountability-api' })
})

app.get('/api/posts', async (_request, response, next) => {
  try {
    response.json(await readData())
  } catch (error) {
    next(error)
  }
})

app.post('/api/posts/:postId/requests', async (request, response, next) => {
  try {
    const { userId, type, question } = request.body
    if (!userId || !type || !question?.trim()) {
      return response.status(400).json({ error: 'userId, type, and question are required.' })
    }

    const data = await readData()
    const post = data.posts.find((item) => item.id === request.params.postId)
    if (!post) return response.status(404).json({ error: 'Post not found.' })
    if (!post.accountable) return response.status(400).json({ error: 'This post is not eligible for context requests.' })
    if (post.requests.some((item) => item.userId === userId)) {
      return response.status(409).json({ error: 'This user has already requested context.' })
    }

    post.requests.push({ userId, type, question: question.trim(), createdAt: new Date().toISOString() })
    await saveData(data)
    response.status(201).json({
      requestCount: post.requests.length,
      publiclyVisible: post.requests.length >= requestThreshold,
    })
  } catch (error) {
    next(error)
  }
})

app.post('/api/posts/:postId/response', async (request, response, next) => {
  try {
    const {
      explanation,
      responseType = '',
      sourceLink = '',
      sources = [],
      documents = [],
      evidenceNote = '',
      label = '',
    } = request.body
    if (!explanation?.trim()) return response.status(400).json({ error: 'An explanation is required.' })

    const data = await readData()
    const post = data.posts.find((item) => item.id === request.params.postId)
    if (!post) return response.status(404).json({ error: 'Post not found.' })

    post.response = {
      responseType,
      explanation: explanation.trim(),
      sourceLink,
      sources,
      documents,
      evidenceNote,
      label,
      createdAt: new Date().toISOString(),
    }
    await saveData(data)
    response.status(201).json(post.response)
  } catch (error) {
    next(error)
  }
})

app.post('/api/posts/:postId/reports', async (request, response, next) => {
  try {
    const data = await readData()
    const post = data.posts.find((item) => item.id === request.params.postId)
    if (!post) return response.status(404).json({ error: 'Post not found.' })

    post.reports ||= []
    post.reports.push({
      userId: request.body.userId || 'anonymous',
      type: 'misuse',
      note: request.body.note || 'Submitted for observer review.',
      reviewed: false,
      createdAt: new Date().toISOString(),
    })
    await saveData(data)
    response.status(201).json({ queued: true })
  } catch (error) {
    next(error)
  }
})

app.patch('/api/posts/:postId/review', async (request, response, next) => {
  try {
    const data = await readData()
    const post = data.posts.find((item) => item.id === request.params.postId)
    if (!post) return response.status(404).json({ error: 'Post not found.' })

    post.reviewedAt = new Date().toISOString()
    await saveData(data)
    response.json({ reviewedAt: post.reviewedAt })
  } catch (error) {
    next(error)
  }
})

app.use((error, _request, response, _next) => {
  console.error(error)
  response.status(500).json({ error: 'Unexpected server error.' })
})

app.listen(port, () => {
  console.log(`Adaptive accountability API listening on http://localhost:${port}`)
})

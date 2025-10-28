import { NextResponse } from 'next/server'
import { execFile } from 'child_process'
import path from 'path'

export async function POST(request: Request) {
  try {
    const body = await request.json()
    const { function: funcName, args = [] } = body

    if (!funcName) {
      return NextResponse.json({ error: 'missing function name' }, { status: 400 })
    }

    const scriptPath = path.join(process.cwd(), 'run_report.py')

    return await new Promise((resolve) => {
      const cp = execFile(process.env.PYTHON || 'python', [scriptPath, funcName, ...args], { cwd: process.cwd() }, (err, stdout, stderr) => {
        if (err) {
          resolve(NextResponse.json({ error: 'execution error', message: err.message, stderr }, { status: 500 }))
          return
        }

        try {
          const parsed = JSON.parse(stdout)
          resolve(NextResponse.json(parsed))
        } catch (e) {
          resolve(NextResponse.json({ error: 'invalid python output', stdout }))
        }
      })
    })
  } catch (e: any) {
    return NextResponse.json({ error: 'invalid request', message: e.message }, { status: 400 })
  }
}

"use client"
import { useEffect, useRef } from "react"
import * as THREE from "three"
import { getGraph } from "@/services/graph"

export default function Graph3D() {
  const canvasRef = useRef<HTMLDivElement>(null)
  useEffect(() => {
    if (!canvasRef.current) return
    const width = canvasRef.current.clientWidth
    const height = 520
    const scene = new THREE.Scene()
    const camera = new THREE.PerspectiveCamera(60, width / height, 0.1, 1000)
    camera.position.z = 60
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true })
    renderer.setSize(width, height)
    canvasRef.current.appendChild(renderer.domElement)
    const light = new THREE.PointLight(0x3A86FF, 2)
    light.position.set(20, 20, 20)
    scene.add(light)
    const group = new THREE.Group()
    scene.add(group)
    getGraph().then(data => {
      const nodes = data.nodes || []
      const edges = data.edges || []
      const positions: Record<string, THREE.Vector3> = {}
      nodes.forEach((n: any, i: number) => {
        const geo = new THREE.SphereGeometry(1.6, 16, 16)
        const mat = new THREE.MeshBasicMaterial({ color: 0x3A86FF, transparent: true, opacity: 0.8 })
        const mesh = new THREE.Mesh(geo, mat)
        const x = Math.sin(i) * 20
        const y = Math.cos(i * 0.7) * 12
        const z = Math.cos(i) * 18
        mesh.position.set(x, y, z)
        positions[String(n.id)] = new THREE.Vector3(x, y, z)
        group.add(mesh)
      })
      edges.forEach((e: any) => {
        const a = positions[String(e.source)]
        const b = positions[String(e.target)]
        if (!a || !b) return
        const points = [a, b]
        const geo = new THREE.BufferGeometry().setFromPoints(points)
        const mat = new THREE.LineBasicMaterial({ color: 0x9bbcf9, transparent: true, opacity: 0.6 })
        const line = new THREE.Line(geo, mat)
        group.add(line)
      })
    })
    const animate = () => { group.rotation.y += 0.001; renderer.render(scene, camera); requestAnimationFrame(animate) }
    animate()
    const onResize = () => { const w = canvasRef.current?.clientWidth || width; renderer.setSize(w, height); camera.aspect = w / height; camera.updateProjectionMatrix() }
    window.addEventListener("resize", onResize)
    return () => { window.removeEventListener("resize", onResize); renderer.dispose() }
  }, [])
  return <div ref={canvasRef} className="w-full" />
}
import * as React from "react"
import Link from "next/link"
import {
  Sidebar,
  SidebarContent,
  SidebarHeader,
  SidebarRail,
} from "@/components/ui/sidebar"

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  return (
    <Sidebar {...props}>
      <SidebarHeader>
        <div className="flex items-center gap-2 px-2 py-4">
          <span className="text-2xl font-extrabold tracking-tight text-blue-700 font-sans">Splitter</span>
        </div>
      </SidebarHeader>
      <SidebarContent>
        <nav className="flex flex-col gap-2 mt-2 px-2">
          <Link
            href="/"
            className="text-base font-medium text-gray-700 hover:text-blue-700 transition-colors rounded px-2 py-1"
          >
            Dashboard
          </Link>
          <Link
            href="/"
            className="text-base font-medium text-gray-700 hover:text-blue-700 transition-colors rounded px-2 py-1"
          >
            Participating Hospitals
          </Link>
          <Link
            href="/about"
            className="text-base font-medium text-gray-700 hover:text-blue-700 transition-colors rounded px-2 py-1"
          >
            About
          </Link>
          <a
            href="https://github.com/your-org/your-repo"
            target="_blank"
            rel="noopener noreferrer"
            className="text-base font-medium text-gray-700 hover:text-blue-700 transition-colors rounded px-2 py-1"
          >
            Github Repo
          </a>
          <a
            href="http://127.0.0.1:8000/docs"
            target="_blank"
            rel="noopener noreferrer"
            className="text-base font-medium text-gray-700 hover:text-blue-700 transition-colors rounded px-2 py-1"
          >
            API Docs
          </a>
        </nav>
      </SidebarContent>
      <SidebarRail />
    </Sidebar>
  )
}

"use client"

import { useState } from "react"
import { Sidebar } from "@/components/sidebar"
import { MainContent } from "@/components/main-content"

export function CallCenterLayout() {
  const [activeSection, setActiveSection] = useState<string | null>(null)
  const [activeSubSection, setActiveSubSection] = useState<string | null>(null)
  const [openTabs, setOpenTabs] = useState<Array<{ section: string; subSection: string; id: string }>>([])

  const handleNavigate = (section: string, subSection: string) => {
    const tabId = `${section}-${subSection}`
    const existingTab = openTabs.find((tab) => tab.id === tabId)

    if (!existingTab) {
      setOpenTabs([...openTabs, { section, subSection, id: tabId }])
    }

    setActiveSection(section)
    setActiveSubSection(subSection)
  }

  const handleCloseTab = (tabId: string) => {
    const updatedTabs = openTabs.filter((tab) => tab.id !== tabId)
    setOpenTabs(updatedTabs)

    const closingTab = openTabs.find((tab) => tab.id === tabId)
    if (closingTab && activeSection === closingTab.section && activeSubSection === closingTab.subSection) {
      if (updatedTabs.length > 0) {
        const lastTab = updatedTabs[updatedTabs.length - 1]
        setActiveSection(lastTab.section)
        setActiveSubSection(lastTab.subSection)
      } else {
        setActiveSection(null)
        setActiveSubSection(null)
      }
    }
  }

  const handleTabClick = (section: string, subSection: string) => {
    setActiveSection(section)
    setActiveSubSection(subSection)
  }

  return (
    <div className="flex h-screen bg-background">
      <Sidebar activeSection={activeSection} activeSubSection={activeSubSection} onNavigate={handleNavigate} />
      <MainContent
        activeSection={activeSection}
        activeSubSection={activeSubSection}
        openTabs={openTabs}
        onCloseTab={handleCloseTab}
        onTabClick={handleTabClick}
      />
    </div>
  )
}

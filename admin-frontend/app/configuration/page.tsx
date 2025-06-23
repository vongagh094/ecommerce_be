"use client"

import { useState } from "react"
import { useToast } from "@/hooks/use-toast"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Switch } from "@/components/ui/switch"
import { Badge } from "@/components/ui/badge"
import { Settings, Save, Plus, Edit, Trash2, Eye, EyeOff, ImageIcon } from "lucide-react"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"

interface Banner {
  id: string
  title: string
  imageUrl: string
  linkUrl: string
  isActive: boolean
}

export default function Configuration() {
  const [activeTab, setActiveTab] = useState("general")
  const { toast } = useToast()

  // System Settings
  const [settings, setSettings] = useState({
    siteName: "AirBnB Admin",
    contactEmail: "admin@airbnb.com",
    commissionRate: "5",
  })

  // Banner Management
  const [banners, setBanners] = useState<Banner[]>([
    {
      id: "1",
      title: "Summer Sale 2024",
      imageUrl: "/placeholder.svg?height=200&width=800",
      linkUrl: "/catalog",
      isActive: true,
    },
    {
      id: "2",
      title: "New Properties Available",
      imageUrl: "/placeholder.svg?height=200&width=800",
      linkUrl: "/catalog",
      isActive: true,
    },
  ])

  const [bannerModal, setBannerModal] = useState({
    open: false,
    mode: "add" as "add" | "edit",
    banner: null as Banner | null,
  })

  const [bannerForm, setBannerForm] = useState({
    title: "",
    imageUrl: "",
    linkUrl: "",
    isActive: true,
  })

  const handleSaveSettings = () => {
    toast({
      title: "Settings Saved",
      description: "Configuration has been updated successfully.",
    })
  }

  const handleAddBanner = () => {
    setBannerForm({ title: "", imageUrl: "", linkUrl: "", isActive: true })
    setBannerModal({ open: true, mode: "add", banner: null })
  }

  const handleEditBanner = (banner: Banner) => {
    setBannerForm({
      title: banner.title,
      imageUrl: banner.imageUrl,
      linkUrl: banner.linkUrl,
      isActive: banner.isActive,
    })
    setBannerModal({ open: true, mode: "edit", banner })
  }

  const handleSaveBanner = () => {
    if (!bannerForm.title || !bannerForm.imageUrl) {
      toast({
        title: "Error",
        description: "Please fill in title and image URL.",
        variant: "destructive",
      })
      return
    }

    if (bannerModal.mode === "add") {
      const newBanner: Banner = {
        id: Date.now().toString(),
        ...bannerForm,
      }
      setBanners([...banners, newBanner])
      toast({
        title: "Banner Added",
        description: "New banner has been created successfully.",
      })
    } else if (bannerModal.banner) {
      setBanners(banners.map((b) => (b.id === bannerModal.banner!.id ? { ...bannerModal.banner!, ...bannerForm } : b)))
      toast({
        title: "Banner Updated",
        description: "Banner has been updated successfully.",
      })
    }

    setBannerModal({ open: false, mode: "add", banner: null })
  }

  const handleDeleteBanner = (bannerId: string) => {
    setBanners(banners.filter((b) => b.id !== bannerId))
    toast({
      title: "Banner Deleted",
      description: "Banner has been deleted successfully.",
    })
  }

  const toggleBannerStatus = (bannerId: string) => {
    setBanners(banners.map((b) => (b.id === bannerId ? { ...b, isActive: !b.isActive } : b)))
    toast({
      title: "Status Updated",
      description: "Banner status has been updated.",
    })
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Configuration</h1>
          <div className="text-sm text-gray-500">Home &gt; Configuration</div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex space-x-8 border-b">
        <button
          className={`pb-2 ${
            activeTab === "general"
              ? "border-b-2 border-blue-500 text-blue-600 font-medium"
              : "text-gray-500 hover:text-gray-700"
          }`}
          onClick={() => setActiveTab("general")}
        >
          General Settings
        </button>
        <button
          className={`pb-2 ${
            activeTab === "banners"
              ? "border-b-2 border-blue-500 text-blue-600 font-medium"
              : "text-gray-500 hover:text-gray-700"
          }`}
          onClick={() => setActiveTab("banners")}
        >
          Homepage Banners
        </button>
      </div>

      {/* General Settings Tab */}
      {activeTab === "general" && (
        <div className="max-w-2xl">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Settings className="w-5 h-5" />
                System Configuration
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="siteName">Site Name</Label>
                  <Input
                    id="siteName"
                    value={settings.siteName}
                    onChange={(e) => setSettings({ ...settings, siteName: e.target.value })}
                  />
                </div>
                <div>
                  <Label htmlFor="contactEmail">Contact Email</Label>
                  <Input
                    id="contactEmail"
                    type="email"
                    value={settings.contactEmail}
                    onChange={(e) => setSettings({ ...settings, contactEmail: e.target.value })}
                  />
                </div>
              </div>

              <div>
                <Label htmlFor="commissionRate">Commission Rate (%)</Label>
                <Input
                  id="commissionRate"
                  type="number"
                  value={settings.commissionRate}
                  onChange={(e) => setSettings({ ...settings, commissionRate: e.target.value })}
                  className="max-w-32"
                />
              </div>

              <Button onClick={handleSaveSettings} className="w-full">
                <Save className="w-4 h-4 mr-2" />
                Save Settings
              </Button>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Banner Management Tab */}
      {activeTab === "banners" && (
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold">Homepage Banners</h2>
            <Button onClick={handleAddBanner}>
              <Plus className="w-4 h-4 mr-2" />
              Add Banner
            </Button>
          </div>

          <Card>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>PREVIEW</TableHead>
                  <TableHead>TITLE</TableHead>
                  <TableHead>LINK</TableHead>
                  <TableHead>STATUS</TableHead>
                  <TableHead>ACTIONS</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {banners.map((banner) => (
                  <TableRow key={banner.id}>
                    <TableCell>
                      <div className="w-20 h-12 bg-gray-200 rounded overflow-hidden">
                        <img
                          src={banner.imageUrl || "/placeholder.svg"}
                          alt={banner.title}
                          className="w-full h-full object-cover"
                        />
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="font-medium">{banner.title}</div>
                    </TableCell>
                    <TableCell>
                      <div className="text-sm text-gray-500 max-w-48 truncate">{banner.linkUrl}</div>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center gap-2">
                        <Badge
                          className={banner.isActive ? "bg-green-100 text-green-800" : "bg-gray-100 text-gray-800"}
                        >
                          {banner.isActive ? "Active" : "Inactive"}
                        </Badge>
                        <Button size="sm" variant="ghost" onClick={() => toggleBannerStatus(banner.id)}>
                          {banner.isActive ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                        </Button>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center gap-2">
                        <Button size="sm" variant="outline" onClick={() => handleEditBanner(banner)}>
                          <Edit className="w-4 h-4" />
                        </Button>
                        <Button size="sm" variant="destructive" onClick={() => handleDeleteBanner(banner.id)}>
                          <Trash2 className="w-4 h-4" />
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </Card>
        </div>
      )}

      {/* Add/Edit Banner Modal */}
      <Dialog open={bannerModal.open} onOpenChange={(open) => setBannerModal({ ...bannerModal, open })}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <ImageIcon className="w-5 h-5" />
              {bannerModal.mode === "add" ? "Add Banner" : "Edit Banner"}
            </DialogTitle>
            <DialogDescription>
              {bannerModal.mode === "add" ? "Create a new banner for homepage." : "Update banner information."}
            </DialogDescription>
          </DialogHeader>

          <div className="space-y-4">
            <div>
              <Label htmlFor="bannerTitle">Title</Label>
              <Input
                id="bannerTitle"
                value={bannerForm.title}
                onChange={(e) => setBannerForm({ ...bannerForm, title: e.target.value })}
                placeholder="Enter banner title"
              />
            </div>

            <div>
              <Label htmlFor="bannerImage">Image URL</Label>
              <Input
                id="bannerImage"
                value={bannerForm.imageUrl}
                onChange={(e) => setBannerForm({ ...bannerForm, imageUrl: e.target.value })}
                placeholder="Enter image URL"
              />
            </div>

            <div>
              <Label htmlFor="bannerLink">Link URL</Label>
              <Input
                id="bannerLink"
                value={bannerForm.linkUrl}
                onChange={(e) => setBannerForm({ ...bannerForm, linkUrl: e.target.value })}
                placeholder="Enter destination URL"
              />
            </div>

            <div className="flex items-center justify-between">
              <div>
                <Label htmlFor="bannerActive">Active</Label>
                <p className="text-sm text-gray-500">Show banner on homepage</p>
              </div>
              <Switch
                id="bannerActive"
                checked={bannerForm.isActive}
                onCheckedChange={(checked) => setBannerForm({ ...bannerForm, isActive: checked })}
              />
            </div>

            {bannerForm.imageUrl && (
              <div>
                <Label>Preview</Label>
                <div className="mt-2 border rounded-lg overflow-hidden">
                  <img
                    src={bannerForm.imageUrl || "/placeholder.svg"}
                    alt="Banner preview"
                    className="w-full h-32 object-cover"
                  />
                </div>
              </div>
            )}
          </div>

          <DialogFooter>
            <Button variant="outline" onClick={() => setBannerModal({ ...bannerModal, open: false })}>
              Cancel
            </Button>
            <Button onClick={handleSaveBanner}>
              <Save className="w-4 h-4 mr-2" />
              {bannerModal.mode === "add" ? "Add Banner" : "Update Banner"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}

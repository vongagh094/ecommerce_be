"use client"

import { useState } from "react"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Checkbox } from "@/components/ui/checkbox"
import { FolderPlus, Tag } from "lucide-react"

interface AddToCatalogModalProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  productName: string
  onConfirm: (category: string, featured: boolean) => void
}

const categories = [
  { value: "residential", label: "Residential Properties" },
  { value: "commercial", label: "Commercial Properties" },
  { value: "vacation", label: "Vacation Rentals" },
  { value: "luxury", label: "Luxury Properties" },
]

export function AddToCatalogModal({ open, onOpenChange, productName, onConfirm }: AddToCatalogModalProps) {
  const [category, setCategory] = useState("")
  const [featured, setFeatured] = useState(false)
  const [isLoading, setIsLoading] = useState(false)

  const handleConfirm = async () => {
    if (!category) return

    setIsLoading(true)
    await new Promise((resolve) => setTimeout(resolve, 1000)) // Simulate API call
    onConfirm(category, featured)
    setIsLoading(false)
    onOpenChange(false)
    setCategory("")
    setFeatured(false)
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
              <FolderPlus className="w-4 h-4 text-blue-600" />
            </div>
            Add to Catalog
          </DialogTitle>
          <DialogDescription>
            Add "{productName}" to a catalog category to organize and promote it better.
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="category">Select Category *</Label>
            <Select value={category} onValueChange={setCategory}>
              <SelectTrigger>
                <SelectValue placeholder="Choose a category" />
              </SelectTrigger>
              <SelectContent>
                {categories.map((cat) => (
                  <SelectItem key={cat.value} value={cat.value}>
                    {cat.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="flex items-center space-x-2">
            <Checkbox id="featured" checked={featured} onCheckedChange={(checked) => setFeatured(checked as boolean)} />
            <Label htmlFor="featured" className="flex items-center gap-2">
              <Tag className="w-4 h-4" />
              Mark as Featured Property
            </Label>
          </div>

          <div className="p-3 bg-blue-50 rounded-lg">
            <div className="text-sm text-blue-700">
              Featured properties get priority placement in search results and category listings.
            </div>
          </div>
        </div>

        <DialogFooter className="flex gap-2">
          <Button variant="outline" onClick={() => onOpenChange(false)} disabled={isLoading}>
            Cancel
          </Button>
          <Button onClick={handleConfirm} disabled={isLoading || !category} className="bg-blue-600 hover:bg-blue-700">
            {isLoading ? "Adding..." : "Add to Catalog"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}

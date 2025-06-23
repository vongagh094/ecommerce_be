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
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Edit } from "lucide-react"

interface EditCatalogModalProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  catalog: {
    id: string
    name: string
    description: string
    type: string
  }
  onConfirm: (id: string, name: string, description: string, type: string) => void
}

const catalogTypes = [
  { value: "residential", label: "Residential Properties" },
  { value: "commercial", label: "Commercial Properties" },
  { value: "vacation", label: "Vacation Rentals" },
  { value: "luxury", label: "Luxury Properties" },
  { value: "budget", label: "Budget Accommodations" },
]

export function EditCatalogModal({ open, onOpenChange, catalog, onConfirm }: EditCatalogModalProps) {
  const [name, setName] = useState(catalog.name)
  const [description, setDescription] = useState(catalog.description)
  const [type, setType] = useState(catalog.type)
  const [isLoading, setIsLoading] = useState(false)

  const handleConfirm = async () => {
    if (!name || !type) return

    setIsLoading(true)
    await new Promise((resolve) => setTimeout(resolve, 1000)) // Simulate API call
    onConfirm(catalog.id, name, description, type)
    setIsLoading(false)
    onOpenChange(false)
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
              <Edit className="w-4 h-4 text-blue-600" />
            </div>
            Edit Catalog
          </DialogTitle>
          <DialogDescription>Update the catalog information and settings.</DialogDescription>
        </DialogHeader>

        <div className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="name">Catalog Name *</Label>
            <Input id="name" placeholder="Enter catalog name" value={name} onChange={(e) => setName(e.target.value)} />
          </div>

          <div className="space-y-2">
            <Label htmlFor="type">Catalog Type *</Label>
            <Select value={type} onValueChange={setType}>
              <SelectTrigger>
                <SelectValue placeholder="Select catalog type" />
              </SelectTrigger>
              <SelectContent>
                {catalogTypes.map((t) => (
                  <SelectItem key={t.value} value={t.value}>
                    {t.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="description">Description</Label>
            <Textarea
              id="description"
              placeholder="Describe this catalog category..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              rows={3}
            />
          </div>
        </div>

        <DialogFooter className="flex gap-2">
          <Button variant="outline" onClick={() => onOpenChange(false)} disabled={isLoading}>
            Cancel
          </Button>
          <Button
            onClick={handleConfirm}
            disabled={isLoading || !name || !type}
            className="bg-blue-600 hover:bg-blue-700"
          >
            {isLoading ? "Updating..." : "Update Catalog"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}

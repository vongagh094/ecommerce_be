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
import { AlertTriangle } from "lucide-react"

interface DeleteCatalogModalProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  catalog: {
    id: string
    name: string
    itemCount: number
  }
  onConfirm: (id: string) => void
}

export function DeleteCatalogModal({ open, onOpenChange, catalog, onConfirm }: DeleteCatalogModalProps) {
  const [isLoading, setIsLoading] = useState(false)

  const handleConfirm = async () => {
    setIsLoading(true)
    await new Promise((resolve) => setTimeout(resolve, 1000)) // Simulate API call
    onConfirm(catalog.id)
    setIsLoading(false)
    onOpenChange(false)
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <div className="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center">
              <AlertTriangle className="w-4 h-4 text-red-600" />
            </div>
            Delete Catalog
          </DialogTitle>
          <DialogDescription>
            Are you sure you want to delete "{catalog.name}"? This action cannot be undone.
          </DialogDescription>
        </DialogHeader>

        <div className="p-4 bg-red-50 rounded-lg">
          <div className="flex items-start gap-2">
            <AlertTriangle className="w-4 h-4 text-red-600 mt-0.5" />
            <div className="text-sm text-red-700">
              <div className="font-medium">Warning:</div>
              <div>
                This catalog contains {catalog.itemCount} items. Deleting it will remove all associated properties from
                this category.
              </div>
            </div>
          </div>
        </div>

        <DialogFooter className="flex gap-2">
          <Button variant="outline" onClick={() => onOpenChange(false)} disabled={isLoading}>
            Cancel
          </Button>
          <Button onClick={handleConfirm} disabled={isLoading} variant="destructive">
            {isLoading ? "Deleting..." : "Delete Catalog"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}

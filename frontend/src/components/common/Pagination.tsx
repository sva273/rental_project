import { motion } from 'framer-motion'

interface PaginationProps {
  currentPage: number
  totalPages: number
  onPageChange: (page: number) => void
  hasNext: boolean
  hasPrevious: boolean
}

const Pagination = ({ currentPage, totalPages, onPageChange, hasNext, hasPrevious }: PaginationProps) => {
  if (totalPages <= 1) return null

  const getPageNumbers = () => {
    const pages: (number | string)[] = []
    const maxVisible = 5

    if (totalPages <= maxVisible) {
      for (let i = 1; i <= totalPages; i++) {
        pages.push(i)
      }
    } else {
      if (currentPage <= 3) {
        for (let i = 1; i <= 4; i++) {
          pages.push(i)
        }
        pages.push('...')
        pages.push(totalPages)
      } else if (currentPage >= totalPages - 2) {
        pages.push(1)
        pages.push('...')
        for (let i = totalPages - 3; i <= totalPages; i++) {
          pages.push(i)
        }
      } else {
        pages.push(1)
        pages.push('...')
        for (let i = currentPage - 1; i <= currentPage + 1; i++) {
          pages.push(i)
        }
        pages.push('...')
        pages.push(totalPages)
      }
    }

    return pages
  }

  return (
    <motion.div 
      className="flex items-center justify-center gap-3 mt-12"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <motion.button
        onClick={() => onPageChange(currentPage - 1)}
        disabled={!hasPrevious}
        whileHover={{ scale: hasPrevious ? 1.05 : 1 }}
        whileTap={{ scale: hasPrevious ? 0.95 : 1 }}
        className="px-6 py-3 glass rounded-xl hover:bg-white/80 disabled:opacity-50 disabled:cursor-not-allowed transition-all font-semibold luxury-border"
      >
        Previous
      </motion.button>

      <div className="flex gap-2">
        {getPageNumbers().map((page, index) => {
          if (page === '...') {
            return (
              <span key={`ellipsis-${index}`} className="px-4 py-2 text-white/70 text-lg">
                ...
              </span>
            )
          }

          const pageNum = page as number
          const isActive = pageNum === currentPage

          return (
            <motion.button
              key={pageNum}
              onClick={() => onPageChange(pageNum)}
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              className={`px-5 py-3 rounded-xl font-bold transition-all ${
                isActive
                  ? 'luxury-gradient text-white shadow-lg glow-effect'
                  : 'glass hover:bg-white/80 text-white'
              }`}
            >
              {pageNum}
            </motion.button>
          )
        })}
      </div>

      <motion.button
        onClick={() => onPageChange(currentPage + 1)}
        disabled={!hasNext}
        whileHover={{ scale: hasNext ? 1.05 : 1 }}
        whileTap={{ scale: hasNext ? 0.95 : 1 }}
        className="px-6 py-3 glass rounded-xl hover:bg-white/80 disabled:opacity-50 disabled:cursor-not-allowed transition-all font-semibold luxury-border"
      >
        Next
      </motion.button>
    </motion.div>
  )
}

export default Pagination


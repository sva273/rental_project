import { motion } from 'framer-motion'

interface PropertyTypeSelectorProps {
  value: string
  onChange: (value: string) => void
}

const PropertyTypeSelector = ({ value, onChange }: PropertyTypeSelectorProps) => {
  const types = [
    { value: '', label: 'All Types' },
    { value: 'apartment', label: 'Apartment' },
    { value: 'house', label: 'House' },
    { value: 'studio', label: 'Studio' },
  ]

  return (
    <div className="flex flex-wrap gap-3">
      {types.map((type) => (
        <motion.button
          key={type.value}
          type="button"
          onClick={() => onChange(type.value)}
          whileHover={{ scale: 1.05, y: -2 }}
          whileTap={{ scale: 0.95 }}
          className={`px-6 py-3 rounded-xl font-semibold transition-all luxury-border ${
            value === type.value
              ? 'luxury-gradient text-black shadow-lg glow-effect'
              : 'glass-dark text-amber-400 hover:bg-amber-400/10'
          }`}
        >
          <span>{type.label}</span>
        </motion.button>
      ))}
    </div>
  )
}

export default PropertyTypeSelector


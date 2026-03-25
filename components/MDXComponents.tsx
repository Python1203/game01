import TOCInline from 'pliny/ui/TOCInline'
import Pre from 'pliny/ui/Pre'
import BlogNewsletterForm from 'pliny/ui/BlogNewsletterForm'
import type { MDXComponents } from 'mdx/types'
import Image from './Image'
import CustomLink from './Link'
import TableWrapper from './TableWrapper'
import AffiliateCardWrapper from './AffiliateCardWrapper'
import AffiliateGrid from './AffiliateGrid'
import TaoBaoTokenPopup from './TaoBaoTokenPopup'
import AllianceCard from './AllianceCard'
import AllianceGrid from './AllianceGrid'

export const components: MDXComponents = {
  Image,
  TOCInline,
  a: CustomLink,
  pre: Pre,
  table: TableWrapper,
  BlogNewsletterForm,
  AffiliateCard: AffiliateCardWrapper,
  AffiliateGrid,
  TaoBaoTokenPopup,
  AllianceCard,
  AllianceGrid,
}

export {
  AffiliateCardWrapper as AffiliateCard,
  AffiliateGrid,
  TaoBaoTokenPopup,
  AllianceCard,
  AllianceGrid,
}

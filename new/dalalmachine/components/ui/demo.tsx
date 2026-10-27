"use client";
import React from "react";
import { TestimonialsColumn, TestimonialItem } from "./testimonials-columns-1";
import { motion } from "motion/react";

const testimonials: TestimonialItem[] = [
  {
    text: "Sourced a 1,600T Voronezh hot forging press under Dalal Machine's High Seas Sales structure. Saved over 18% in duty & forex markup. Commercial crankshaft production started in 45 days.",
    image: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80",
    name: "Rajesh Patel",
    role: "Managing Director, Premier Forgings Ltd. (Rajkot)",
  },
  {
    text: "The 1,000T Russian knuckle joint coining line standing in Dalal's Pune yard was inspected under live power by our technical team. Unmatched transparency and certified tolerances.",
    image: "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&auto=format&fit=crop&q=80",
    name: "Arvind K. Mehta",
    role: "VP Operations, Apex Transmission Components (Pune)",
  },
  {
    text: "We urgently needed an Erfurt 800T stamping press for an OEM automotive bracket contract. Mr. Vinit Dalal coordinated European disconnection, port offloading, and hydraulic trailer transit.",
    image: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&auto=format&fit=crop&q=80",
    name: "Gurpreet Singh",
    role: "Technical Director, Punjab Stamping Lines (Ludhiana)",
  },
  {
    text: "Zero foreign currency exposure by buying under High Seas in Indian Rupees (INR). Direct Bill of Entry in our company name ensured 100% full GST input tax credit without dispute.",
    image: "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=150&auto=format&fit=crop&q=80",
    name: "Mahendra V. Joshi",
    role: "Chairman, Western Heavy Forgings (Ahmedabad GIDC)",
  },
  {
    text: "Imported a heavy CNC floor-type horizontal boring machine from Germany. Foundation blueprints and electrical wiring schematics matched 100% with original OEM delivery.",
    image: "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=150&auto=format&fit=crop&q=80",
    name: "S. R. Ramanathan",
    role: "Head of Procurement, Titan Engine Components (Coimbatore)",
  },
  {
    text: "Dalal's technical partnership with OMPI India for pneumatic clutch-brake retrofitting gave our 400T friction screw press complete modern safety compliance and rapid cycle times.",
    image: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80",
    name: "Vikramaditya Rathore",
    role: "Director, Bharat Auto Axles (Faridabad Hub)",
  },
  {
    text: "Procured a 4,000T heavy press line from Russia. Dalal handled 120-ton single-piece crane lifting at Nhava Sheva port and multi-axle puller road clearance through 3 states.",
    image: "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=150&auto=format&fit=crop&q=80",
    name: "Sanjay Singhania",
    role: "Plant Head, Singhania Industrial Forgings (Jamshedpur)",
  },
  {
    text: "Their Pune yard inventory is unmatched. We inspected the Li Chin 200T mechanical C-frame press on Tuesday, signed High Seas documents on Wednesday, and had it running by next week.",
    image: "https://images.unsplash.com/photo-1560250097-0b93528c311a?w=150&auto=format&fit=crop&q=80",
    name: "Hemant Deshmukh",
    role: "Chief Engineer, Maharashtra Precision Stamps (Chakan)",
  },
  {
    text: "Working with Mr. Vinit Dalal for 15+ years. Their pre-purchase ultrasonic testing and non-cracked frame guarantee removes all risks of purchasing second-hand heavy machinery.",
    image: "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=150&auto=format&fit=crop&q=80",
    name: "Rameshwar Goel",
    role: "Managing Director, Continental Heavy Forgings (NCR)",
  },
];

const firstColumn = testimonials.slice(0, 3);
const secondColumn = testimonials.slice(3, 6);
const thirdColumn = testimonials.slice(6, 9);

export const Testimonials = () => {
  return (
    <section className="bg-background my-20 relative overflow-hidden py-16">
      <div className="container z-10 mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.1, ease: [0.16, 1, 0.3, 1] }}
          viewport={{ once: true }}
          className="flex flex-col items-center justify-center max-w-[580px] mx-auto text-center"
        >
          <div className="flex justify-center">
            <div className="border border-amber-500/30 bg-amber-500/10 text-amber-600 font-semibold text-xs tracking-wider uppercase py-1 px-4 rounded-full">
              Client Verifications
            </div>
          </div>

          <h2 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-extrabold tracking-tight mt-5 text-foreground">
            What India&apos;s Leading Forging Directors Say
          </h2>
          <p className="text-center mt-4 text-muted-foreground text-sm sm:text-base">
            Verified feedback from Managing Directors, VP Operations, and Plant Technical Heads across India&apos;s auto manufacturing hubs.
          </p>
        </motion.div>

        <div className="flex justify-center gap-6 mt-12 [mask-image:linear-gradient(to_bottom,transparent,black_20%,black_80%,transparent)] max-h-[740px] overflow-hidden">
          <TestimonialsColumn testimonials={firstColumn} duration={15} />
          <TestimonialsColumn testimonials={secondColumn} className="hidden md:block" duration={19} />
          <TestimonialsColumn testimonials={thirdColumn} className="hidden lg:block" duration={17} />
        </div>
      </div>
    </section>
  );
};

export default Testimonials;
